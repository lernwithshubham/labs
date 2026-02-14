# Demo: Distributed Observability with Prometheus & Grafana

This lab demonstrates how to implement an industry-standard monitoring stack. We will deploy **Prometheus** and **Grafana** on a central Monitoring Server, and configure them to scrape real-time metrics from a remote Production Server running **Node Exporter**.

## 📋 Prerequisites
You need **Two AWS EC2 Instances** (Ubuntu 22.04 or 24.04).

* **VM 1: Monitoring Server** (`t2.medium`)
    * *Security Group:* Open Ports `22` (SSH), `3000` (Grafana), and `9090` (Prometheus).
* **VM 2: Production Target** (`t2.micro`)
    * *Security Group:* Open Ports `22` (SSH) and `9100` (Node Exporter).

---

## 🚀 Part 1: Instrument the Target Server (VM 2)

First, we install the agent that translates Linux system metrics into an HTTP endpoint.

1. SSH into **VM 2**.
2. Install Node Exporter:
```bash
sudo apt-get update -y
sudo apt-get install -y prometheus-node-exporter
```
3. Verify it is running by viewing the raw metrics:
```bash
curl http://localhost:9100/metrics
```

## 🧠 Part 2: Deploy the Observability Stack (VM 1)

Next, we install the time-series database and the visualization dashboard on the central server.

1. SSH into VM 1.
2. Install Prometheus:
```bash
sudo apt-get update -y
sudo apt-get install -y prometheus
```
3. Install Grafana:
```bash
sudo apt-get install -y apt-transport-https software-properties-common wget
sudo mkdir -p /etc/apt/keyrings/
wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor | sudo tee /etc/apt/keyrings/grafana.gpg > /dev/null
echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | sudo tee /etc/apt/sources.list.d/grafana.list

sudo apt-get update -y
sudo apt-get install -y grafana
sudo systemctl enable --now grafana-server
```

## 🔗 Part 3: Configure Remote Scraping (VM 1)

We must tell Prometheus where to find the target server.

1. On VM 1, edit the Prometheus configuration file:
```bash
sudo vi /etc/prometheus/prometheus.yml
```
2. Scroll to the bottom and add a new job under scrape_configs containing the Private IP of VM 2:
```bash
scrape_configs:
  - job_name: prometheus
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'production_web_server'
    static_configs:
      - targets: ['<PRIVATE_IP_OF_VM_2>:9100']
```
3. Restart Prometheus:
```bash
sudo systemctl restart prometheus
```

## 📊 Part 4: Build the Grafana Dashboard

1. Open your browser and go to http://<PUBLIC_IP_OF_VM_1>:3000.
2. Login with admin / admin.
3. Connect the Data:
* Go to Connections > Data Sources > Add data source.
* Select Prometheus.
* Set the URL to http://localhost:9090.
* Click Save & test.

4. Import the Dashboard:
* Click the + icon in the top right -> Import dashboard.
* Enter the ID `1860` and click Load.
* Select your Prometheus data source at the bottom and click Import.

## ⚔️ Part 5: The Load Test Simulation

We will simulate a traffic spike or runaway process on the target server to watch the dashboard react in real-time.

1. SSH back into VM 2 (The Target).
2. Install and run a stress test to max out 2 CPU cores for 60 seconds:
```bash
sudo apt-get install -y stress
stress --cpu 2 --timeout 60
```
3. Quickly switch back to your Grafana browser tab and watch the CPU and System Load graphs spike!

