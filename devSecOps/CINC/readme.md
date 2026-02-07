# Demo: Automated Compliance with CINC Auditor

This demonstration shows how to implement **Compliance-as-Code**. We use **CINC Auditor** (InSpec) to scan a Linux server and ensure it meets specific security and configuration standards.

## 📋 Scenario
We define a **"Web Server Hardening"** profile with three rules:
1.  **Required Software:** `nginx` must be installed.
2.  **File Integrity:** `/etc/shadow` must be owned by `root`.
3.  **Forbidden Files:** `/tmp/backdoor.sh` must NOT exist.

## ✅ Prerequisites
* An Ubuntu AWS EC2 Instance.
* Root/Sudo access.

---

## 🚀 Part 1: Install CINC Auditor

Run the following command to install the tool:

```bash
curl -L [https://omnitruck.cinc.sh/install.sh](https://omnitruck.cinc.sh/install.sh) | sudo bash -s -- -P cinc-auditor
```

## 🛠️ Part 2: Setup "Non-Compliant" State

We intentionally break the server to demonstrate the detection capabilities.

```bash

# 1. Create a fake "backdoor" file
touch /tmp/backdoor.sh

# 2. Ensure Nginx is missing
sudo apt-get remove -y nginx

```

## 📝 Part 3: Create Compliance Profile

Initialize the profile and Edit controls/example.rb and replace the content:

```bash

cinc-auditor init profile web-server-security
cd web-server-security

```

## 🔍 Part 4: Run the Audit (Fail)

Execute the compliance check

```bash

sudo cinc-auditor exec .

```
## 🛡️ Part 5: Remediate and Verify (Pass)

Fix the security issues manually and run the audit again:

```bash

# 1. Install Nginx
sudo apt-get update && sudo apt-get install -y nginx

# 2. Delete the backdoor
rm /tmp/backdoor.sh

sudo cinc-auditor exec .

```


## 📊 Part 6: Reporting (Audit Evidence)

For official audits, we generate a standalone HTML report instead of just looking at terminal logs.

### 1. Generate the Report
Run the auditor with the `--reporter` flag:

```bash
sudo cinc-auditor exec . --reporter html:report.html

```

View the reports

python3 -m http.server 8000