# Demo: Kubernetes Policy Enforcement with OPA

This demonstration shows how to use **Open Policy Agent (OPA)** to validate Kubernetes manifests against security and reliability policies *before* deployment.

## 📋 Scenario
We enforce two policies on a Kubernetes Deployment:
1.  **No "Latest" Tags:** To ensure immutable and predictable deployments.
2.  **Minimum Replicas:** To ensure High Availability (HA) requirements.

## ✅ Prerequisites
* Linux/Mac Machine (or AWS EC2).
* `curl` installed.

---

## 🚀 Part 1: Install OPA

Run the following commands to install the OPA binary:

```bash
curl -L -o opa [https://openpolicyagent.org/downloads/latest/opa_linux_amd64_static](https://openpolicyagent.org/downloads/latest/opa_linux_amd64_static)
chmod 755 ./opa
sudo mv opa /usr/local/bin/
opa version
```

## ❌ Part 2: The Vulnerable Manifest

Create a file named deployment.yaml. This file violates our policies

```bash

touch deployment.yaml

```

## 📜 Part 3: The OPA Policy (Rego)

Create a file named rules.rego. This defines our compliance logic

```bash

touch rules.rego

```

## 🔍 Part 4: Run the Check

Evaluate the YAML file against the Rego policy

```bash

opa eval --format pretty --input deployment.yaml --data rules.rego "data.kubernetes.validating.deny"

```

## 🛡️ Part 5: The Fix

Update deployment.yaml to comply with the rules

* Set replicas: 3.
* Set image: nginx:1.21.

Run the scan again:

```bash

opa eval --format pretty --input deployment.yaml --data rules.rego "data.kubernetes.validating.deny"

```