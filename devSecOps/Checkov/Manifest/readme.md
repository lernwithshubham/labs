# Demo: Kubernetes Security Scanning with Checkov

This demonstration shows how to secure **Kubernetes Manifests** (YAML) by scanning them for misconfigurations before deployment. We focus on preventing **Privileged Containers** and enforcing **Non-Root** execution.

## 📋 Scenario
We define a simple Kubernetes Pod that contains common security mistakes:
1.  **Privileged Mode:** Gives the container full access to the host machine.
2.  **Root User:** The container runs as the root user by default.
3.  **Default Namespace:** Deployed into the global default namespace.

## ✅ Prerequisites
* An Ubuntu machine.
* Docker installed and running.

---

## 🚀 Part 1: Setup

### 1. Create Workspace
Create a folder for our Kubernetes files.

```bash
mkdir k8s-demo
cd k8s-demo

```

----

## ❌ Part 2: The "Vulnerable" Manifest

### 1. Create the YAML File
Create a file named pod.yaml

```bash
touch pod.yaml
```

----

## 🔍 Part 3: Run the Security Scan

We use the Checkov Docker container to scan the current directory

```bash

docker run --rm --tty --volume $(pwd):/tf bridgecrew/checkov --directory /tf

```

## 🛡️ Part 4: Remediation (The Fix)

### 1. Edit the File

```bash

touch pod.yaml

```
## ✅ Part 5: Verification

```bash

docker run --rm --tty --volume $(pwd):/tf bridgecrew/checkov --directory /tf

```