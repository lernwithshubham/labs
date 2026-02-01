# DAST Automation with OWASP ZAP (Docker)

This guide demonstrates how to set up a Dynamic Application Security Testing (DAST) pipeline on a "headless" Linux server (e.g., AWS EC2 Ubuntu). We use the official **OWASP ZAP Docker image** to scan a test application (`demo.testfire.net`) and generate an HTML vulnerability report.

## Prerequisites
* A Linux environment (Ubuntu/Debian recommended).
* Root or `sudo` access.
* Port **8000** allowed in your firewall/AWS Security Group (for viewing the report).

---

## 1. Environment Setup

First, we need to install Docker, as we will run ZAP as a container to avoid complex dependency management.

```bash
# 1. Update your package list
sudo apt-get update

# 2. Install Docker
sudo apt-get install -y docker.io

# 3. Start the Docker service and enable it to launch on boot
sudo systemctl start docker
sudo systemctl enable docker

# 4. (Optional) Allow your current user to run Docker without 'sudo'
# NOTE: You must log out and log back in for this to take effect.
sudo usermod -aG docker $USER

##
docker run -v $(pwd):/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable zap-full-scan.py \
    -t http://demo.testfire.net \
    -r test_report.html

##
python3 -m http.server 8000

