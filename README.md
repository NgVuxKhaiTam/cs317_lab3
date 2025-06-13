# CS317 Lab3: RUL Prediction Service with Monitoring & Logging

This repository implements a Remaining Useful Life (RUL) prediction API using FastAPI and TensorFlow, coupled with an end-to-end observability stack (Prometheus, Grafana, Alertmanager, Filebeat).

## Table of Contents

* [Features](#features)
* [Prerequisites](#prerequisites)
* [Repository Structure](#repository-structure)
* [Configuration](#configuration)
* [Building & Running](#building--running)
* [Usage](#usage)
* [Monitoring & Dashboards](#monitoring--dashboards)
* [Alerting](#alerting)
* [Troubleshooting](#troubleshooting)

## Features

* FastAPI service for RUL prediction
* TensorFlow model with pre-trained weights
* Prometheus instrumentation (API, model, server)
* Grafana dashboards (provisioned automatically)
* Alertmanager alerts to Telegram
* Unified logging (stdout, stderr, syslog, file, Filebeat)

## Prerequisites

* Docker & Docker Compose
* Telegram bot token and valid chat ID
* (Optional) Elasticsearch or Loki for logs

## Repository Structure

```text
cs317_lab3/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── main.py
├── logging_config.py
├── model.py
├── preprocess_data.py
├── train_FD004.txt
├── monitoring/
│   ├── prometheus/
│   │   ├── prometheus.yml
│   │   └── alert_rules.yml
│   ├── alertmanager/
│   │   └── alertmanager.yml
│   ├── grafana/
│   │   └── provisioning/
│   │       └── datasources/
│   │           └── prometheus.yml
│   └── filebeat/
│       └── filebeat.yml
├── logs/                # host-mounted logs
└── README.md            
```

## Configuration

1. Edit `monitoring/alertmanager/alertmanager.yml` and set your Telegram `<YOUR_BOT_TOKEN>` and `<CHAT_ID>`.
2. Review Prometheus configs in `monitoring/prometheus/`.
3. Verify Grafana provisioning under `monitoring/grafana/provisioning/datasources/`.
4. Adjust logging settings in `logging_config.py` and `monitoring/filebeat/filebeat.yml`.

## Building & Running

1. From project root:

   ```bash
   cd cs317_lab3
   ```
2. Build and start all services:

   ```bash
   docker-compose up --build
   ```

## Usage

### Health Check

```bash
curl http://localhost:15000/
```

### Prediction API

```bash
curl -X POST "http://localhost:15000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "sensor_2": 445.0,
    "sensor_3": 549.68,
    "sensor_4": 1343.43,
    "sensor_7": 1112.93,
    "sensor_8": 3.91,
    "sensor_9": 5.7,
    "sensor_11": 137.36,
    "sensor_12": 2211.86,
    "sensor_13": 8311.32,
    "sensor_14": 1.01,
    "sensor_15": 41.69,
    "sensor_17": 129.78,
    "sensor_20": 2387.99,
    "sensor_21": 8074.83
  }'
```

### Metrics Endpoint

```bash
curl http://localhost:15000/metrics
```

### Viewing Logs

* Application: `tail -f logs/app.log`
* Syslog: `tail -f /var/log/syslog`

## Monitoring & Dashboards

* **Prometheus UI**: [http://localhost:9090](http://localhost:9090)
* **Grafana UI**: [http://localhost:3000](http://localhost:3000) (admin/admin)
* Import Node Exporter Dashboard (ID 1860)
* Import or create API & Model dashboard (JSON at `monitoring/grafana/dashboards/api_model.json`)

## Alerting

* High error rate (>50% in 5m) triggers Telegram alert
* Low confidence (<0.6 predictions) triggers Telegram alert
* Manage at Alertmanager UI: [http://localhost:9093](http://localhost:9093)

## Troubleshooting

1. Check rule status: [http://localhost:9090/rules](http://localhost:9090/rules)
2. Inspect logs:

   ```bash
   docker logs prometheus
   docker logs alertmanager
   docker logs rul-prediction-service
   ```
3. Test Telegram API:

   ```bash
   curl -s 'https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates'
   curl -s 'https://api.telegram.org/bot<YOUR_BOT_TOKEN>/sendMessage?chat_id=<CHAT_ID>&text=hello'
   ```
4. Grafana provisioning issues: `docker logs grafana`

---

## Video

[![Watch the video](https://drive.google.com/drive/folders/19koIzIvi7LIpKiaKg8X4FdIFUfmtoo5A?usp=sharing)](https://drive.google.com/drive/folders/19koIzIvi7LIpKiaKg8X4FdIFUfmtoo5A?usp=sharing)
