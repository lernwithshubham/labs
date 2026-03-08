import re
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --- Setup ---
LOG_FILE = "application.log"
OUT_DIR = Path("outputs"); OUT_DIR.mkdir(exist_ok=True)
CSV_PATH = OUT_DIR / "log_events.csv"
PNG_PATH = OUT_DIR / "log_trends.png"

# --- Regex to extract fields: timestamp, level, message ---
pattern = re.compile(r"^(?P<timestamp>\S+ \S+),\d+ (?P<level>\w+) (?P<message>.*)$")

records = []
with open(LOG_FILE, "r") as f:
    for line in f:
        match = pattern.match(line.strip())
        if match:
            records.append(match.groupdict())

# --- Convert to DataFrame ---
df = pd.DataFrame(records)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["level"] = df["level"].str.upper()

# --- Save structured logs ---
df.to_csv(CSV_PATH, index=False)

# --- Count events by severity ---
counts = df["level"].value_counts()

# --- Plot severity trend over time ---
plt.figure(figsize=(10,5))
for level, group in df.groupby("level"):
    plt.plot(group["timestamp"], [level]*len(group), marker="o", linestyle="none", label=level)
plt.title("Log Severity Trend")
plt.xlabel("Time")
plt.ylabel("Severity Level")
plt.legend()
plt.tight_layout()
plt.savefig(PNG_PATH, dpi=120)

# --- Print summary ---
print("=== Log Analysis Summary ===")
print(f"Saved structured log CSV: {CSV_PATH}")
print(f"Saved severity trend chart: {PNG_PATH}")
print("Event counts by level:")
print(counts.to_string())
