import re
import json
import pandas as pd
from pathlib import Path
from datetime import timedelta

CFG = json.load(open("config.json", "r"))
LOG_FILE = Path(CFG["paths"]["log_file"]).resolve()
PRED_CSV = Path(CFG["paths"]["pred_alerts_csv"]).resolve()
WINDOW = int(CFG.get("correlation_window", 10))

OUT_DIR = Path("outputs"); OUT_DIR.mkdir(exist_ok=True)
CSV_PATH = OUT_DIR / "root_cause_candidates.csv"
TXT_PATH = OUT_DIR / "root_cause_summary.txt"

pattern = re.compile(
    r"^(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),\d+\s+(?P<level>\w+)\s+(?P<message>.*)$"
)
records = []
with open(LOG_FILE, "r", encoding="utf-8") as f:
    for line in f:
        m = pattern.match(line.strip())
        if m:
            records.append(m.groupdict())

logs = pd.DataFrame(records)
if logs.empty:
    pd.DataFrame(columns=["alert_time","error_time","error_message","proximity_minutes"]).to_csv(CSV_PATH, index=False)
    with open(TXT_PATH, "w", encoding="utf-8") as f:
        f.write("Root Cause Analysis - no logs parsed; cannot correlate.\n")
    print("=== Root Cause Analysis Summary ===")
    print(f"Saved candidate CSV: {CSV_PATH}")
    print(f"Saved text summary: {TXT_PATH}")
    raise SystemExit(0)

logs["timestamp"] = pd.to_datetime(logs["timestamp"])
logs["level"] = logs["level"].str.upper()

pred = pd.read_csv(PRED_CSV)
alerts = pred[pred["alert"] == 1].copy()
base_day = logs["timestamp"].min().floor("D")
alerts["t"] = alerts["t"].astype(int)
alerts["alert_time"] = base_day + pd.to_timedelta(alerts["t"], unit="m")

candidates = []
for _, a in alerts.iterrows():
    alert_time = a["alert_time"]
    window_start = alert_time - timedelta(minutes=WINDOW)
    window_end = alert_time + timedelta(minutes=WINDOW)
    nearby = logs[(logs["timestamp"] >= window_start) & (logs["timestamp"] <= window_end)]
    errors = nearby[nearby["level"] == "ERROR"]
    for _, err in errors.iterrows():
        candidates.append({
            "alert_time": alert_time,
            "error_time": err["timestamp"],
            "error_message": err["message"],
            "proximity_minutes": abs((err["timestamp"] - alert_time).total_seconds() / 60.0)
        })

if candidates:
    cands_df = pd.DataFrame(candidates).sort_values(by="proximity_minutes")
else:
    cands_df = pd.DataFrame(columns=["alert_time","error_time","error_message","proximity_minutes"])

cands_df.to_csv(CSV_PATH, index=False)

lines = [f"Root Cause Analysis - correlation window {WINDOW}m"]
if cands_df.empty:
    lines.append("No candidate errors correlated with predictive alerts.")
else:
    lines.append("Top candidate error messages:")
    for _, r in cands_df.head(5).iterrows():
        lines.append(f"- {r['error_message']} (error at {r['error_time']}, near alert {r['alert_time']})")

with open(TXT_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print("=== Root Cause Analysis Summary ===")
print(f"Saved candidate CSV: {CSV_PATH}")
print(f"Saved text summary: {TXT_PATH}")
if not cands_df.empty:
    print("\n".join(lines))
