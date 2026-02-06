# DAST Demo: OWASP ZAP on AWS

This guide walks through setting up a **Dynamic Application Security Testing (DAST)** pipeline on an AWS Ubuntu instance. We will launch a vulnerable target application (**OWASP Juice Shop**) and scan it using the lightweight **OWASP ZAP Baseline Scan**.

## Prerequisites
* [cite_start]**AWS EC2 Instance:** Ubuntu 20.04 or 22.04[cite: 168].
* [cite_start]**Security Group Rules:** Ensure the following "Inbound Rules" are open[cite: 173, 174]:
    * **Port 22:** SSH (Your IP)
    * **Port 3000:** Custom TCP (Your IP) - To view the target app.
    * **Port 8000:** Custom TCP (Your IP) - To view the report.

---

## Part 1: Environment Setup

[cite_start]First, update the system and install Docker, which is required to run both the target app and the scanner[cite: 238, 239].

```bash
# 1. Update system packages
sudo apt-get update

# 2. Install Docker
sudo apt-get install -y docker.io

```
Launch the Target Application

# 1. Run Juice Shop in the background (detached mode)
```bash
docker run -d --name juice-shop -p 3000:3000 bkimminich/juice-shop
```

# 2. Verify it is running
curl -I http://0.0.0.0:3000

Run the DAST Scan (OWASP ZAP)
```bash
mkdir -p ~/zap-demo
cd ~/zap-demo

chmod 777 $(pwd) # if you are working as a root user
```
Execute the Scan Run the scanner
```bash
docker run --rm -t --network="host" \
  -v $(pwd):/zap/wrk/:rw \
  ghcr.io/zaproxy/zaproxy:stable \
  zap-baseline.py \
  -t http://0.0.0.0:3000 \
  -r zap_report.html


python3 -m http.server 8000

```
