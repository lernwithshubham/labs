# Trivy Security Scanner - Live Class Demos

This demo contains the instructions and commands for a live demonstration of **Trivy**, a comprehensive security scanner. These demos cover **Software Composition Analysis (SCA)** across different technology stacks (Python & Java).

## Prerequisites
* A Linux environment (Ubuntu 20.04/22.04 recommended).
* `sudo` access.
* No prior tools (Docker, Java, Python) are required; Trivy scans static files.

---

## Part 1: Installation (Interactive)
Copy and paste these commands to install the latest version of Trivy.

```bash
# 1. Update system packages
sudo apt-get update

# 2. Install Trivy (One-line official installer)
curl -sfL [https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh](https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh) | sudo sh -s -- -b /usr/local/bin

# 3. Verify installation
trivy --version

# 4. Run the Scan
trivy fs .

# 5. Scan container images
trivy image python:3.4-alpine

---

## Part 6: Reporting
**Objective:** specific vulnerability reports to share with developers or auditors.

### 1. Download the HTML Template
Trivy requires a template file to generate HTML reports. Download the official template first.

```bash
curl -o html.tpl https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/html.tpl

trivy fs --format template --template "@html.tpl" --output report.html .


python3 -m http.server 8000

---

Open in Browser Navigate to the following URL (replace Public-IP with your AWS instance IP): http://<YOUR_AWS_PUBLIC_IP>:8000/report.html