import json
import os
import re
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

CFG = json.load(open("config.json", "r"))
SERVICE_NAME = CFG.get("service_name", "Spooler")
WIN = int(CFG.get("error_spike_window_minutes", 5))
THRESH = int(CFG.get("error_spike_threshold", 2))
REQ_PREBREACH = bool(CFG.get("require_prebreach_alert", False))

LOG_FILE = Path(CFG["paths"]["log_file"]).resolve()
PRED_CSV = Path(CFG["paths"]["pred_alerts_csv"]).resolve()

OUT_DIR = Path("outputs"); OUT_DIR.mkdir(exist_ok=True)
INC_DIR = OUT_DIR / "incidents"; INC_DIR.mkdir(exist_ok=True)
RUNBOOK_AUDIT = OUT_DIR / "runbook_audit.log"

def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def write_audit(msg: str) -> None:
    with open(RUNBOOK_AUDIT, "a", encoding="utf-8") as f:
        f.write(f"{now_iso()} | {msg}\n")

error_spike = False
err_examples = []

if LOG_FILE.exists():
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        raw_lines = [ln.rstrip("\n") for ln in f if ln.strip()]

    pattern = re.compile(
        r"^(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),\d+\s+(?P<lvl>\w+)\s+(?P<msg>.*)$"
    )
    rows = [m.groupdict() for ln in raw_lines if (m := pattern.match(ln))]

    if rows:
        parts = pd.DataFrame(rows)
        parts["ts"] = pd.to_datetime(parts["ts"], errors="coerce")
        parts["lvl"] = parts["lvl"].str.upper()
        parts = parts.dropna(subset=["ts"])

        latest_ts = parts["ts"].max()
        cutoff = latest_ts - timedelta(minutes=WIN)

        recent = parts[parts["ts"] >= cutoff]
        recent_errors = recent[recent["lvl"] == "ERROR"]

        error_spike = len(recent_errors) >= THRESH
        err_examples = recent_errors["msg"].head(3).tolist()
    else:
        write_audit(f"LOG_PARSE_EMPTY: No lines matched format in {LOG_FILE}")
else:
    write_audit(f"LOG_NOT_FOUND: {LOG_FILE}")

prebreach_ok = True
prebreach_hits = 0

if PRED_CSV.exists():
    try:
        pred = pd.read_csv(PRED_CSV)
        if "alert" in pred.columns:
            prebreach_hits = int(pred["alert"].sum())
            prebreach_ok = (prebreach_hits > 0) or (not REQ_PREBREACH)
        else:
            write_audit(f"PRED_CSV_NO_ALERT_COL: {PRED_CSV}")
    except Exception as e:
        write_audit(f"PRED_CSV_READ_ERR: {PRED_CSV} err={e}")
else:
    write_audit(f"PRED_CSV_NOT_FOUND: {PRED_CSV}")

should_incident = bool(error_spike and prebreach_ok)

if should_incident:
    inc_id = f"INC-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6].upper()}"
    severity = "SEV-2" if prebreach_hits > 0 else "SEV-3"
    short_desc = f"{severity} | Error spike in last {WIN}m (>= {THRESH}); prebreach alerts: {prebreach_hits}"

    incident = {
        "incident_id": inc_id,
        "created_utc": now_iso(),
        "severity": severity,
        "service": SERVICE_NAME,
        "signals": {
            "error_spike_window_minutes": WIN,
            "error_spike_threshold": THRESH,
            "error_spike_observed": int(error_spike),
            "prebreach_alerts": prebreach_hits
        },
        "examples": err_examples,
        "status": "OPEN",
        "next_actions": [
            "Run remediation script to restart the service",
            "Verify health checks after restart",
            "Create post-incident ticket if recurring"
        ]
    }

    inc_path = INC_DIR / f"{inc_id}.json"
    with open(inc_path, "w", encoding="utf-8") as f:
        json.dump(incident, f, indent=2)

    chatops = OUT_DIR / "chatops_summary.txt"
    with open(chatops, "w", encoding="utf-8") as f:
        f.write(f"[{incident['severity']}] {incident['incident_id']} | {short_desc}\n")
        f.write(f"Service: {SERVICE_NAME} | Examples: {err_examples[:2]}\n")
        f.write(f"Incident JSON: {inc_path}\n")

    remediate = OUT_DIR / "remediate_restart_service.ps1"
    with open(remediate, "w", encoding="utf-8") as f:
        f.write(f"$svc = '{SERVICE_NAME}'\n")
        f.write("Write-Host \"Stopping service...\"\n")
        f.write("Stop-Service -Name $svc -Force -ErrorAction SilentlyContinue\n")
        f.write("Start-Sleep -Seconds 3\n")
        f.write("Write-Host \"Starting service...\"\n")
        f.write("Start-Service -Name $svc -ErrorAction Continue\n")
        f.write("Write-Host \"Service status:\"; Get-Service -Name $svc | Select-Object Status, Name\n")

    write_audit(f"INCIDENT_OPENED id={inc_id} sev={severity} examples={len(err_examples)}")
    print("=== Incident Created ===")
    print(f"Incident: {inc_path}")
    print(f"ChatOps summary: {chatops}")
    print(f"Remediation script: {remediate}")
else:
    print("No incident opened (error spike or pre-breach conditions not met).")
    write_audit("NO_INCIDENT: conditions not met")

print(f"Audit log: {RUNBOOK_AUDIT}")
