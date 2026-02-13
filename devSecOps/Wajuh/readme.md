# Demo: Kubernetes Node Security Monitoring with Wazuh SIEM

This demonstration illustrates how to build a distributed **Security Operations Center (SOC)** to monitor Kubernetes infrastructure. We deploy a centralized **Wazuh SIEM Manager** and use a lightweight OS-level agent to detect critical misconfigurations and unauthorized tampering on a Kubernetes Worker/Master node.

## 📋 Scenario Overview
Instead of just relying on Kubernetes API logs, we use **File Integrity Monitoring (FIM)** to watch the underlying host operating system. 

We will:
1.  Deploy a Wazuh Manager on a central SIEM server.
2.  Deploy a Wazuh Agent on a target Kubernetes node.
3.  Configure the agent to monitor highly sensitive Kubernetes directories (e.g., `/etc/kubernetes/manifests` and `/var/lib/kubelet/pods`).
4.  Simulate a host-level misconfiguration (world-writable mounts) and manifest tampering to trigger a critical SOC alert.

## ✅ Prerequisites
This lab requires two separate Linux environments (e.g., AWS EC2 instances running Ubuntu 22.04/24.04).

* **VM 1: Security Server (Wazuh Manager)**
    * **Size:** Minimum `t3.medium` (4GB RAM required for the indexer).
    * **Network:** Allow inbound TCP ports `22` (SSH), `443` (Dashboard), `1514` (Agent Data), and `1515` (Agent Enrollment).
* **VM 2: Target Server (Kubernetes Node)**
    * **Size:** `t2.micro` or any existing node in your cluster.
    * **Network:** Allow inbound TCP port `22` (SSH).

---

## 🚀 Part 1: Deploy the Central SIEM (VM 1)

First, we build the "brain" of the SOC. This script automatically installs the Wazuh Indexer, Manager, and Dashboard.

1. SSH into **VM 1**.
2. Download and run the automated installer:
```bash
curl -sO https://packages.wazuh.com/4.7/wazuh-install.sh
sudo bash wazuh-install.sh -a --ignore-check
```
3. Important: Wait 5-8 minutes for the installation to complete. Copy the auto-generated admin password printed at the end of the terminal output.

## 🔗 Part 2: Connect the Target Node (VM 2)

Next, we install the security sensor on our Kubernetes node.

1. Open your web browser and navigate to https://<VM_1_PUBLIC_IP>.
2. Log in using the admin credentials.
3. Navigate to Wazuh > Agents > Deploy new agent.
4. Fill out the wizard (Debian/Ubuntu, amd64, enter VM 1's IP) and copy the generated installation command.
5. SSH into VM 2 and paste the command to install the agent.
6. Start the agent:

```bash
sudo systemctl daemon-reload
sudo systemctl enable wazuh-agent
sudo systemctl start wazuh-agent
```

## 🛡️ Part 3: Configure K8s Node Monitoring (VM 2)

By default, Wazuh monitors standard Linux directories. We must explicitly tell it to watch Kubernetes core files.

1. On VM 2, open the Wazuh agent configuration:

```bash
sudo vi /var/ossec/etc/ossec.conf
```

2. Locate the <syscheck> block (File Integrity Monitoring) and add the following directories to track K8s manifests and running Pod volumes:

```bash
  <directories check_all="yes">/etc/kubernetes/manifests</directories>
  <directories check_all="yes">/var/lib/kubelet/pods</directories>
```
3. Restart the agent to apply the new security policy:

```bash
sudo systemctl restart wazuh-agent
```

## ⚔️ Part 4: The Attack Simulation (VM 2)

We will simulate a scenario where a container is deployed with a highly insecure, world-writable volume mount (a common vector for Container Escapes).

1. On VM 2, try to login root user with incorrect password:

```bash
su root
```
2. On VM 2, navigate to a monitored directory (simulating a Pod's volume mount):

crash schedular pod by making changes in manifest files

## 🚨 Part 5: Incident Response & Detection (VM 1)

Return to the perspective of the SOC Analyst.

1. Open the Wazuh Dashboard in your browser.
2. Navigate to Modules > Security Events.
3. Set the time filter to Last 15 minutes and click Refresh.
4. Look for the critical File Integrity alerts. You will see a specific alert identifying the dangerous configuration:

Alert Details:
```bash
Rule: File is owned by root and has written permissions to anyone.

File: /var/lib/kubelet/pods/a275ee49-444a-48c7-955f-6684e2b6392e/containers/mount-bpffs/7d8748b2
```

