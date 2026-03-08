import os
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt

# Config
RANDOM_SEED = 42
CONTAMINATION = 0.03
OUT_DIR = "outputs"
CSV_PATH = os.path.join(OUT_DIR, "cpu_usage_with_anomalies.csv")
PNG_PATH = os.path.join(OUT_DIR, "anomalies.png")

# Simulated CPU usage data
np.random.seed(RANDOM_SEED)
cpu = np.random.normal(loc=50, scale=5, size=300)
cpu[250:260] = np.random.normal(loc=90, scale=2, size=10)

df = pd.DataFrame({"cpu_usage": cpu})
df.index.name = "timestamp"

# Train Isolation Forest model
model = IsolationForest(contamination=CONTAMINATION, random_state=RANDOM_SEED)
df["anomaly"] = model.fit_predict(df[["cpu_usage"]])

# Save outputs
os.makedirs(OUT_DIR, exist_ok=True)
df.to_csv(CSV_PATH, index=True)

plt.figure(figsize=(12, 6))
plt.plot(df.index, df["cpu_usage"], label="CPU Usage")
an_idx = df.index[df["anomaly"] == -1]
plt.scatter(an_idx, df.loc[an_idx, "cpu_usage"], marker="x", color="red", label="Anomaly")
plt.title("AI-powered Anomaly Detection in CPU Usage")
plt.xlabel("Timestamp")
plt.ylabel("CPU Usage (%)")
plt.legend()
plt.tight_layout()
plt.savefig(PNG_PATH, dpi=120)

# Console summary
total = len(df)
an_count = (df["anomaly"] == -1).sum()
print(f"Total points: {total}")
print(f"Detected anomalies: {an_count}")
print(f"CSV saved to: {CSV_PATH}")
print(f"Chart saved to: {PNG_PATH}")
