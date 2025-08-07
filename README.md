# 🌐 Smart Edge–Cloud Monitor

**Your Environment, Monitored — From the Edge to the Cloud**  
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)  
[![Platform](https://img.shields.io/badge/platform-Raspberry%20Pi-lightgrey)]()  
[![Status](https://img.shields.io/badge/status-In%20Development-yellow)]()

---

## 📖 Overview

The Smart Edge–Cloud Monitor is an IoT system designed to collect real-time environmental data (temperature and humidity) using a Raspberry Pi, and send this data securely to AWS cloud infrastructure for monitoring, logging, and future analysis.

---

## 🌟 Features

- 📡 Sensor-to-Cloud Data Streaming (DHT22 → Pi → AWS IoT Core)
- 🌤 Real-Time Temperature and Humidity Monitoring
- ☁️ Secure Communication over MQTT
- 🗂️ Local Logging with Cloud Sync
- 📊 Cloud Storage with AWS DynamoDB (MVP)
- 📡 Planned Visualization via Web Dashboard

---

## 📁 Project Structure

```bash
smart-edge-cloud-monitor/
├── src/                    # Main application code (Python)
│   └── main.py
├── docs/                   # Documentation
│   ├── PID.txt             # Project Initiation Document (📄 [PID](docs/PID.txt))
│   └── TDD.txt             # Technical Design Document (📄 [TDD](docs/TDD.txt))
├── test/                   # Unit tests and test data
├── hardware/               # Wiring diagrams and pin mappings
├── .gitignore
├── LICENSE
└── README.md               # This file
```

---

## 🚀 Getting Started

### ✅ Prerequisites

- Raspberry Pi 4 or 5 (with RPi OS 64-bit)
- Python 3.9+ installed
- Internet connectivity (Wi-Fi or Ethernet)
- AWS Account + IAM permissions for IoT Core & DynamoDB

### 💻 Clone the Repository

```bash
git clone https://github.com/chrisdudley-dev/smart-edge-cloud-monitor.git
cd smart-edge-cloud-monitor
```

### 🧪 Create Virtual Environment & Install Dependencies

#### On **Windows**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

#### On **macOS / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🔍 Usage Example

```bash
python src/main.py
```

Expected Output:
```json
{
  "timestamp": "2025-08-06T22:11:03Z",
  "temperature_C": 24.6,
  "humidity": 52.4,
  "device_id": "edge-node-001"
}
```

---

## 🧠 System Overview

> 📌 Architecture Diagram (Coming Soon)  
> 📌 Sensor Wiring Diagram (Coming Soon)

---

## 🛣 Roadmap

- [x] Create project structure and GitHub repo
- [x] Draft PID and TDD
- [x] Write README scaffold
- [ ] Integrate DHT22 sensor
- [ ] Implement local data logging
- [ ] Configure AWS IoT Core & DynamoDB
- [ ] Set up MQTT broker
- [ ] Add error handling and edge buffering
- [ ] Finalize unit testing suite
- [ ] Add web-based dashboard (stretch goal)

---

## 📚 Documentation

- [📄 Project Initiation Document (PID)](docs/PID.txt)
- [📄 Technical Design Document (TDD)](docs/TDD.txt)

---

## 🤝 Contributing

Want to contribute? Awesome!  
Help us improve by forking the repo and submitting a pull request.

> CONTRIBUTING.md coming soon...

---

## 📬 Contact

- Chris Dudley – [GitHub](https://github.com/chrisdudley-dev)

---

## 📝 License

This project is licensed under the [Apache 2.0 License](LICENSE).
