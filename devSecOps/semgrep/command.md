# ⚡ Demo Commands Reference




```bash
# Calculate the sum of 10, 20, and 30
python3 cost.py "[10, 20, 30]"

# Injecting __import__('os').system('id') to execute shell commands
python3 cost.py "[__import__('os').system('id'), 0]"

# Scan using the specific "eval-detected" rule
semgrep --config="r/python.lang.security.audit.eval-detected"
