# Host Intrusion Detection System (HIDS)

A machine learning-based intrusion detection system that monitors host systems for security threats in real-time.

## Quick Start

### 1. Install Dependencies

```bash
pip3 install -r requirements.txt
```

### 2. Run Dashboard

```bash
python3 simple_dashboard.py
```

Then open your browser to: **http://localhost:5000**

That's it! The system will:
- ✅ Train a baseline model automatically (first run only)
- ✅ Start real-time monitoring
- ✅ Display metrics and alerts in your browser

---

## Features

- **Real-time Monitoring**: CPU, memory, processes, disk usage
- **ML Anomaly Detection**: Isolation Forest algorithm
- **Web Dashboard**: Clean, simple interface with live graphs
- **Alert System**: Detects suspicious activity
- **No Network Metrics**: Simplified view (can be enabled if needed)

---

## Project Structure

```
sidaan/
├── simple_dashboard.py    # Main dashboard (USE THIS)
├── main.py                # Full CLI interface (advanced)
├── config.py              # Configuration
├── data_collector.py      # System metrics collection
├── feature_engineering.py # Feature extraction
├── ml_models.py           # Machine learning models
├── monitor.py             # Real-time monitoring engine
├── alert_system.py        # Alert management
├── requirements.txt       # Dependencies
├── templates/             # HTML templates
├── models/                # Trained models (auto-created)
└── README.md             # This file
```

---

## Usage

### Start Dashboard (Recommended)

```bash
python3 simple_dashboard.py
```

Open: http://localhost:5000

### Advanced Commands

```bash
# Train model manually
python3 main.py train

# Monitor in terminal
python3 main.py monitor

# Check status
python3 main.py status
```

---

## Configuration

Edit `config.py` to customize:

```python
MODEL_TYPE = 'isolation_forest'   # ML algorithm
CONTAMINATION = 0.1               # Expected anomaly ratio
COLLECTION_INTERVAL = 2           # Seconds between checks
ANOMALY_THRESHOLD = 0.6           # Detection sensitivity
```

---

## API Endpoints

When dashboard is running:

- `GET /api/status` - Current status
- `GET /api/metrics` - Real-time metrics
- `GET /api/alerts` - Recent alerts
- `POST /api/start` - Start monitoring
- `POST /api/stop` - Stop monitoring

---

## Requirements

- Python 3.8+
- macOS / Linux / Windows
- pip3

---

## Troubleshooting

**Port 5000 already in use?**
The system will automatically use port 8080 instead.

**Permission errors on macOS?**
Some metrics require elevated permissions. Run with:
```bash
sudo python3 simple_dashboard.py
```

---

## License

MIT License
