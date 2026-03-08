import os, json
import numpy as np
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt

# --- Setup & Config ---
OUT_DIR = Path("outputs"); OUT_DIR.mkdir(parents=True, exist_ok=True)
CFG = json.load(open("config.json", "r"))

H = int(CFG.get("horizon", 24))
K = float(CFG.get("dynamic_threshold_k", 3.0))
LEEWAY = float(CFG.get("min_alert_leeway", 5.0))
SEED = int(CFG.get("random_seed", 42))

rng = np.random.default_rng(SEED)

# --- Simulated metric (e.g., CPU %) with trend + seasonality + noise ---
n_points = 7 * 24  # 7 days of hourly points
t = np.arange(n_points)
trend = 0.02 * t                      # slow upward drift
season = 8 * np.sin(2 * np.pi * t/24) # daily cycle
noise = rng.normal(0, 2, size=n_points)
metric = 45 + trend + season + noise
metric = np.clip(metric, 0, 100)

df = pd.DataFrame({"metric": metric})
df.index.name = "t"

# --- Feature engineering: lags + rolling stats (sklearn/pandas only) ---
def make_features(s: pd.Series, max_lag: int = 24) -> pd.DataFrame:
    feat = pd.DataFrame({f"lag_{i}": s.shift(i) for i in range(1, max_lag + 1)})
    feat["roll_mean_6"]  = s.rolling(6).mean()
    feat["roll_std_6"]   = s.rolling(6).std().fillna(0)
    feat["roll_mean_24"] = s.rolling(24).mean()
    feat["roll_std_24"]  = s.rolling(24).std().fillna(0)
    return feat

X = make_features(df["metric"], 24)
y = df["metric"]
data = pd.concat([X, y], axis=1).dropna()

X_train = data.iloc[:-H, :-1]
y_train = data.iloc[:-H, -1]

# hold-out to compare (not strictly necessary for alerting, but useful)
X_test  = data.iloc[-H:, :-1]
y_test  = data.iloc[-H:, -1]

# --- Dynamic threshold (μ + K·σ) from training distribution ---
mu = y_train.mean()
sigma = y_train.std(ddof=0)
dynamic_threshold = mu + K * sigma

# --- Train a robust tree-based regressor (no extra libs) ---
model = RandomForestRegressor(n_estimators=400, random_state=SEED, n_jobs=-1)
model.fit(X_train, y_train)

# --- Multi-step forecasting by recursive one-step prediction on lags ---
history = list(df["metric"].values[-24:])
preds = []
for _ in range(H):
    row = {f"lag_{i}": history[-i] for i in range(1, 25)}
    row["roll_mean_6"]  = pd.Series(history[-6:]).mean()
    row["roll_std_6"]   = pd.Series(history[-6:]).std(ddof=0) if len(history) >= 6 else 0
    row["roll_mean_24"] = pd.Series(history[-24:]).mean()
    row["roll_std_24"]  = pd.Series(history[-24:]).std(ddof=0)
    X_row = pd.DataFrame([row])
    yhat = float(model.predict(X_row)[0])
    preds.append(yhat)
    history.append(yhat)

future_idx = np.arange(df.index.max() + 1, df.index.max() + 1 + H)
pred_df = pd.DataFrame({"pred": preds}, index=future_idx)

# --- Alert logic: warn when forecast crosses (threshold - leeway) before actual breach ---
pred_df["threshold"] = dynamic_threshold
pred_df["prebreach_line"] = dynamic_threshold - LEEWAY
pred_df["alert"] = (pred_df["pred"] >= pred_df["prebreach_line"]).astype(int)

# --- Save tabular outputs for pipelines ---
OUT_CSV = OUT_DIR / "predictions_with_alerts.csv"
pred_df.to_csv(OUT_CSV, index_label="t")

# --- Visualize history + forecast + lines + alert markers ---
plt.figure(figsize=(13, 6))
plt.plot(df.index, df["metric"], label="Actual (history)")
plt.plot(pred_df.index, pred_df["pred"], label="Forecast (next H)")
plt.axhline(y=pred_df["threshold"].iloc[0], linestyle="--", label=f"Threshold (μ+{K}σ)")
plt.axhline(y=pred_df["prebreach_line"].iloc[0], linestyle=":", label="Pre-breach line")
alert_idx = pred_df.index[pred_df["alert"] == 1]
plt.scatter(alert_idx, pred_df.loc[alert_idx, "pred"], marker="x", label="Alert")
plt.title("Predictive Monitoring Alerts: Forecast vs Dynamic Threshold")
plt.xlabel("Time index")
plt.ylabel("Metric (%)")
plt.legend()
plt.tight_layout()
OUT_PNG = OUT_DIR / "predictions_chart.png"
plt.savefig(OUT_PNG, dpi=120)

# --- Human-friendly summary for ChatOps/ITSM ---
summary = OUT_DIR / "alerts_summary.txt"
with open(summary, "w") as f:
    f.write(f"Horizon: {len(pred_df)} | Threshold: {dynamic_threshold:.2f} | Pre-breach: {(dynamic_threshold-LEEWAY):.2f}\n")
    alert_points = pred_df[pred_df["alert"] == 1]
    if alert_points.empty:
        f.write("No alerts predicted in the horizon.\n")
    else:
        f.write(f"{len(alert_points)} alert(s) predicted at indexes: {list(alert_points.index)}\n")
        f.write(alert_points[["pred"]].to_string())

print("=== Predictive Alerts Summary ===")
print(f"Saved CSV: {OUT_CSV}")
print(f"Saved chart: {OUT_PNG}")
print(f"Saved summary: {summary}")
alerts = pred_df[pred_df['alert']==1].index.tolist()
print("Predicted alerts at:" if alerts else "No predicted alerts.", alerts if alerts else "")
