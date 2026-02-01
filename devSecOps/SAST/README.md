# Semgrep DevSecOps Demo: Shift-Left Security with Python

This repository demonstrates a "Shift-Left" security workflow. We will write a simple Python utility, exploit a critical vulnerability (Eval Injection), detect it using Semgrep (SAST), and fix it using secure coding practices.

## 🎯 The Scenario
**The Goal:** Build a simple CLI tool that sums up a list of prices provided by a user.
**The Trap:** A "lazy" implementation using Python's `eval()` function opens the door to Remote Code Execution (RCE).
**The Fix:** Replacing the dangerous function with a secure parser (`ast.literal_eval`).

---

## 🛠️ Prerequisites & Setup
This demo runs on a standard Ubuntu VM (e.g., AWS EC2).

### 1. Install Tools
Update the system and install Python, Git, and Semgrep.
```bash
sudo apt update -y
sudo apt install -y git python3 python3-pip pipx

# Install Semgrep via pipx (recommended for Ubuntu)
pipx ensurepath
source ~/.bashrc
pipx install semgrep

### 2. Verification

python3 --version
semgrep --version
