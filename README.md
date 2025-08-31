﻿# ðŸŒ Smart Edgeâ€“Cloud Monitor

**Your Environment, Monitored â€” From the Edge to the Cloud**  
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)  
[![Platform](https://img.shields.io/badge/platform-Raspberry%20Pi-lightgrey)]()  
[![Status](https://img.shields.io/badge/status-In%20Development-yellow)]()

---

## ðŸ“– Overview

The Smart Edgeâ€“Cloud Monitor is an IoT system designed to collect real-time environmental data (temperature and humidity) using a Raspberry Pi, and send this data securely to AWS cloud infrastructure for monitoring, logging, and future analysis.

---

## ðŸŒŸ Features

- ðŸ“¡ Sensor-to-Cloud Data Streaming (DHT22 â†’ Pi â†’ AWS IoT Core)
- ðŸŒ¤ Real-Time Temperature and Humidity Monitoring
- â˜ï¸ Secure Communication over MQTT
- ðŸ—‚ï¸ Local Logging with Cloud Sync
- ðŸ“Š Cloud Storage with AWS DynamoDB (MVP)
- ðŸ“¡ Planned Visualization via Web Dashboard

---

## ðŸ“ Project Structure

```bash
smart-edge-cloud-thermohygrometer/
â”œâ”€â”€ src/                    # Main application code (Python)
â”‚   â”œâ”€â”€ main.py
â”‚   â””â”€â”€ log_sensors_mock.py # Mock temperature/humidity logger
â”œâ”€â”€ docs/                   # Documentation
â”‚   â”œâ”€â”€ PID.txt             # Project Initiation Document
â”‚   â””â”€â”€ TDD.txt             # Technical Design Document
â”œâ”€â”€ test/                   # Unit tests and test data
â”œâ”€â”€ hardware/               # Wiring diagrams and pin mappings
â”œâ”€â”€ requirements.txt        # Edge device dependencies
â”œâ”€â”€ requirements-dev.txt    # Local development + CI dependencies
â”œâ”€â”€ lambda_requirements.txt # AWS Lambda deployment dependencies
â”œâ”€â”€ lambda_local_requirements.txt # AWS Lambda local test dependencies
â”œâ”€â”€ .gitignore
â”œâ”€â”€ LICENSE
â””â”€â”€ README.md               # This file
```

---

## ðŸš€ Getting Started

### âœ… Prerequisites
- Raspberry Pi 4 or 5 (with Raspberry Pi OS 64-bit)
- Python 3.9+ installed
- Internet connectivity (Wi-Fi or Ethernet)
- AWS Account + IAM permissions for IoT Core & DynamoDB

### ðŸ’» Clone the Repository
```bash
git clone https://github.com/chrisdudley-dev/smart-edge-cloud-thermohygrometer.git
cd smart-edge-cloud-thermohygrometer
```

### ðŸ§ª Create Virtual Environment
#### Windows
```powershell
python -m venv venv
venv\Scripts\activate
```
#### macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

---

### ðŸ“¦ Install Dependencies

**For Local Development / CI**  
Includes runtime + testing, linting, and analysis tools.
```bash
pip install -r requirements-dev.txt
```

**For Raspberry Pi Edge Device**  
Minimal runtime dependencies for the Pi itself.  
If using legacy `RPi.GPIO` + `Adafruit_DHT`, uncomment those lines in `requirements.txt` before installing.
```bash
pip install -r requirements.txt
```

**For AWS Lambda Deployment**  
Keep `lambda_requirements.txt` minimal (often empty). Add only extra packages your Lambda handler imports.
```bash
pip install -r lambda_requirements.txt
```

**For Local Testing of Lambda Functions**  
Matches Lambdaâ€™s runtime libraries (including boto3/botocore).
```bash
pip install -r lambda_local_requirements.txt
```

---

## ðŸ” Usage Examples

### Run the main app
From the repo root:
```bash
python src/main.py
```

**Expected Output**
```json
{
  "timestamp": "2025-08-06T22:11:03Z",
  "temperature_C": 24.6,
  "humidity": 52.4,
  "device_id": "edge-node-001"
}
```

---

### Mock Sensor Logger (Day 16â€“17)
Generate realistic mock readings (as if from a DHT22) for local logging, testing, and pipeline exercises.

```bash
# Example: create 60 readings at 2s interval with explicit sensor ID
python src/log_sensors_mock.py --count 60 --interval 2   --device-id edge-node-001 --sensor-id dht22-lab   --output data/sensor_log.jsonl
```

**Sample JSON Lines** (one object per line)
```json
{
  "timestamp": "2025-08-31T12:25:08Z",
  "timestamp_ms": "2025-08-31T12:25:08.788Z",
  "temperature_C": 23.4,
  "humidity": 49.8,
  "device_id": "edge-node-001",
  "sensor_id": "dht22-lab"
}
```

**Flags**
- `--device-id` (default: `edge-node-001`)
- `--sensor-id` (default: `dht22-001`)
- `--count` number of readings (`0` = infinite)
- `--interval` seconds between readings (use `0` for fastest)
- `--output` JSONL file (default: `data/sensor_log.jsonl`)
- `--seed` random seed for reproducibility
- `--self-test` runs built-in smoke tests and exits

> Tip: keep generated logs out of Gitâ€”add this to `.gitignore`:
> ```
> data/
> ```


---

## ðŸ§  System Overview

## Architecture

**Variant A â€” Mosquitto bridge**  
![Mosquitto bridge](docs/architecture/arch_variantA_mosquitto-bridge.png)

**Variant B â€” Direct to AWS**  
![Direct to AWS](docs/architecture/arch_variantB_direct-aws.png)

### Data Flow Sequence

```mermaid
sequenceDiagram
    autonumber

    participant Edge as Edge (Raspberry Pi)
    participant Broker as MQTT Broker
    box AWS Cloud
    participant IoT as AWS IoT Core Rule
    participant L as AWS Lambda
    participant DB as DynamoDB
    participant SNS as SNS Alerts
    end

    %% Publish from edge
    Edge->>Broker: sensor/data, sensor/alerts (JSON, QoS 1)

    %% Choose one deployment
    alt Direct to AWS
        Broker->>IoT: MQTT message (JSON)
    else Mosquitto bridge
        Broker-->>IoT: bridge sensor/#
    end

    %% Cloud processing
    IoT->>L: Rule invocation
    activate L
    par Persist
        L->>DB: Store reading
    and Alert on anomaly
        L->>SNS: Send alert
    end
    deactivate L

    %% Future
    Note over Edge,IoT: Future: OTA/config via Jobs/Shadow
```

> The dashed OTA/config (Jobs/Shadow) path is included in both variants.

> ðŸ“Œ Sensor Wiring Diagram (Coming Soon)

---

## ðŸ›£ Roadmap

- [x] Create project structure and GitHub repo
- [x] Draft PID and TDD
- [x] Write README scaffold
- [x] Add modular dependency files for edge, Lambda, and local dev
- [ ] Integrate DHT22 sensor
- [ ] Implement local data logging
- [ ] Configure AWS IoT Core & DynamoDB
- [ ] Set up MQTT broker
- [ ] Add error handling and edge buffering
- [ ] Finalize unit testing suite
- [ ] Add web-based dashboard (stretch goal)

---

## ðŸ“š Documentation

- [ðŸ“„ Project Initiation Document (PID)](docs/PID.txt)
- [ðŸ“„ Technical Design Document (TDD)](docs/TDD.txt)

---

## ðŸ¤ Contributing

Want to contribute? Awesome!  
Help us improve by forking the repo and submitting a pull request.

> CONTRIBUTING.md coming soon...

---

## ðŸ“¬ Contact

- Chris Dudley â€“ [GitHub](https://github.com/chrisdudley-dev)

---

## ðŸ“ License

This project is licensed under the [Apache 2.0 License](LICENSE).



