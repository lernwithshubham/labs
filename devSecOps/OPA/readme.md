# Open Policy Agent (OPA) - Quick Start Demo

This page contains a simple demonstration of **Open Policy Agent (OPA)** functionality. It guides you through installing the OPA binary on Linux (Ubuntu), defining a basic access control policy using **Rego**, and testing that policy with different inputs.

## Prerequisites

* A Linux environment (e.g., Ubuntu VM on AWS).
* `curl` installed.

## 1. Installation

Run the following commands to download the OPA binary and move it to your system path.

```bash
# 1. Download the OPA binary (v0.60.0)
curl -L -o opa https://openpolicyagent.org/downloads/v0.60.0/opa_linux_amd64_static
# 2. Make the binary executable
chmod 755 ./opa

# 3. Move it to your local bin directory so you can run it globally
sudo mv opa /usr/local/bin/

# 4. Verify installation
opa version


# User: "Bob" (Developer) Action: "delete" Expected Result: false (Denied)

opa eval -i -d policy.rego 'data.play.allow' --input '{"user": "bob", "groups": ["dev"], "action": "delete"}'


# User: "Sarah" (Admin) Action: "delete" Expected Result: true (Allowed)

opa eval -i -d policy.rego 'data.play.allow' --input '{"user": "sarah", "groups": ["admin"], "action": "delete"}'

