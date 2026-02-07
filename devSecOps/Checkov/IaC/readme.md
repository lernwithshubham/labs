# Demo: IaC Security Scanning with Checkov

This demonstration illustrates **"Shift-Left Security"** by scanning Infrastructure as Code (Terraform) for misconfigurations before deployment. We use **Checkov**, a static code analysis tool, to identify and fix security vulnerabilities in AWS resources.

## 📋 Scenario
We define two AWS resources using Terraform:
1.  **S3 Bucket:** Initially configured with public access (High Risk).
2.  **Security Group:** Initially configured to allow SSH (Port 22) from the entire internet (Critical Risk).

We will scan this code, identify the failures, and apply fixes to pass the security check.

## ✅ Prerequisites
* An Ubuntu machine (AWS EC2 or Local).
* Docker installed and running.

---

## 🚀 Part 1: Setup

### 1. Install Docker (If not installed)
If you are on a fresh Ubuntu instance, run these commands to install Docker.

```bash
sudo apt-get update
sudo apt-get install -y docker.io
```
### 2. Create Demo Directory

```bash
mkdir iac-demo
cd iac-demo
```

### 3. Create the Terraform File

```bash
touch main.tf

```
---

## 🚀 Part 2: Setup

### 1. Run the Security Scan
We use the Checkov Docker container to scan the current directory (/tf inside the container).

```bash
docker run --rm --tty --volume $(pwd):/tf bridgecrew/checkov --directory /tf

```
