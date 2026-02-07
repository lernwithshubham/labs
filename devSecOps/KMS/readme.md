# Demo: Secrets Management in CI/CD with AWS Secrets Manager

This page contains a step-by-step guide to implementing secure secrets management on AWS. Instead of hardcoding credentials (like API keys or passwords) into source code, this demo retrieves them dynamically at runtime using **AWS Secrets Manager** and **IAM Roles**.

## 📋 Scenario
We simulate a **Payment Service** application that requires a Stripe API Key to process transactions.
* **The Problem:** Hardcoding the API key in the script is a security risk.
* **The Solution:** The script fetches the key from AWS Secrets Manager only when needed, uses it in memory, and never saves it to disk.

## ✅ Prerequisites
* An active AWS Account.
* An **Ubuntu EC2 Instance** (t2.micro is sufficient) running and accessible via SSH.
* Root (`sudo`) access on the instance.

---

## 🚀 Part 1: AWS Console Setup (IAM Configuration)

Before logging into the server, we must grant the EC2 instance permission to access the "Vault" (Secrets Manager) without using long-term access keys.

### Step 1.1: Create the IAM Role
1.  Log in to the **AWS Management Console**.
2.  Navigate to **IAM** > **Roles** and click **Create role**.
3.  **Trusted Entity Type:** Select **AWS service**.
4.  **Service or Use Case:** Select **EC2** from the dropdown/list.
5.  Click **Next**.
6.  **Add Permissions:** Search for and check the box next to **`SecretsManagerReadWrite`**.
    * *(Note: For production, create a custom policy with least privilege. For this demo, ReadWrite is acceptable.)*
7.  Click **Next**.
8.  **Role Name:** Enter `Payment-Service-Role`.
9.  Click **Create role**.

### Step 1.2: Attach Role to EC2 Instance
1.  Navigate to the **EC2 Console** > **Instances**.
2.  Select your running Ubuntu instance.
3.  Click **Actions** > **Security** > **Modify IAM role**.
4.  In the dropdown, select the `Payment-Service-Role` you just created.
5.  Click **Update IAM role**.

---

## 🛠️ Part 2: Server Configuration

Connect to your EC2 instance via SSH and configure the environment.

### Step 2.1: Configure Region
We do not need to provide `aws_access_key_id` because the IAM Role handles authentication. We only need to set the region.

```bash
# 1. Update system
sudo apt-get update

# 2. Install AWS CLI (if not already installed)
sudo apt-get install -y awscli

# 3. Configure the Region (Must match where you will create the secret, e.g., us-east-2)
aws configure set region us-east-2
```

## 🛠️ Part 3: Create the Secret (The Vault)
We will create a "Production" API key for our payment processor and store it securely in AWS Secrets Manager.

```bash
# 1. Update system

aws secretsmanager create-secret \
    --name prod/stripe/apikey \
    --description "Production API Key for Payment Gateway" \
    --secret-string "sk_live_<alphanumerstring>"

```

## 🛠️ Part 4: The Application (Pipeline Script)
We will create a script that simulates the application. It will:

* Fetch the secret at runtime.
* Validate it exists.
* Mask the output (security best practice).
* Simulate a process using the key.

```bash
# 1. Update system

aws secretsmanager create-secret \
    --name prod/stripe/apikey \
    --description "Production API Key for Payment Gateway" \
    --secret-string "sk_live_<alphanumerstring>"

# 2. Create the Script

vi payment_service.sh

# 3. Run the Application

chmod +x payment_service.sh
./payment_service.sh

```

## 🛠️ Part 5: Secret Rotation (Emergency Scenario)
Imagine the API key was leaked. We need to rotate it immediately without redeploying the code.


```bash
# 1. Update the Secret in AWS

aws secretsmanager put-secret-value \
    --secret-id prod/stripe/apikey \
    --secret-string "sk_new_<alphanumericstring>"

# 2. Re-run the Application

./payment_service.sh

```

## 🛠️ Cleanup

```bash
# 1. Delete the Secret

aws secretsmanager delete-secret --secret-id prod/stripe/apikey --force-delete-without-recovery

# 2. Detach and Delete IAM Role

Go to EC2 Console, select Instance > Actions > Security > Modify IAM role > Select No IAM Role > Update.

Go to IAM Console, find Payment-Service-Role, and delete it.

```
