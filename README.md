# 🗂️ project_1.0 — Project Portfolio

A collection of AI-powered, Python-based projects spanning machine learning, automation, web apps, and more.

> **Repository:** [arshad49/project_1.0](https://github.com/arshad49/project_1.0)

---

## 📁 Project Index

| # | Project | Tech Stack | Type |
|---|---------|------------|------|
| 1 | [ATS CODE](#1-ats-code--resume-ranker) | Python, Streamlit, scikit-learn | ML / NLP |
| 2 | [Host Intrusion System](#2-host-intrusion-system) | Python, Flask, scikit-learn | ML / Security |
| 3 | [Startup Idea Analyser](#3-startup-idea-analyser) | n8n, AI | Automation |
| 4 | [Crop Disease Detection System](#4-crop-disease-detection-system) | FastAPI, Deep Learning | AI / Vision |
| 5 | [Dental Clinic RAG](#5-dental-clinic-rag) | Django, Gemini AI | RAG / Chatbot |
| 6 | [Fake News Detector](#6-fake-news-detector) | Flask, Gemini AI | AI / NLP |
| 7 | [Folow — WhatsApp Follow-up System](#7-folow--whatsapp-follow-up-system) | FastAPI, Supabase, n8n | Automation |
| 8 | [RAG Proto](#8-rag-proto) | Flask, Ollama (Llama 3.2) | RAG / Chatbot |
| 9 | [Rai Predictor](#9-rai-predictor--kerala-rain-predictor) | Flask, scikit-learn | ML / Weather |
| 10 | [Simple CRM](#10-simple-crm--salescrm) | React, Google Sheets | CRM / Web |
| 11 | [Voice Assistant](#11-voice-assistant--jarvisnova) | Flask, SocketIO, Speech | Voice AI |

---

## 1. ATS CODE — Resume Ranker

**Path:** `ATS CODE/`

A lightweight **Applicant Tracking System** that ranks resumes against a job description using TF-IDF and cosine similarity.

### Features
- Paste any job description as input
- Upload multiple PDF resumes at once
- Ranks candidates by relevance score (highest match first)
- Clean tabular output via Streamlit

### Tech Stack
| Layer | Technology |
|-------|------------|
| Frontend | Streamlit |
| PDF Parsing | pypdf |
| ML / Ranking | scikit-learn (TF-IDF + Cosine Similarity) |
| Data Display | pandas |

### How It Works
1. Job description and uploaded resumes are extracted as plain text
2. All documents are vectorized using TF-IDF
3. Cosine similarity is computed between the job description and each resume
4. Results are sorted and displayed from best to worst match

### Project Structure
```
ATS CODE/
├── ats.py             # Main Streamlit application
└── README_3.md        # Project documentation
```

### Setup
```bash
pip install streamlit pandas pypdf scikit-learn
streamlit run ats.py
# Open: http://localhost:8501
```

---

## 2. Host Intrusion System

**Path:** `Host Itrution System/`

A machine learning-based **Host Intrusion Detection System (HIDS)** that monitors a system in real-time and raises alerts on suspicious activity.

### Features
- Real-time monitoring: CPU, memory, processes, disk usage
- ML Anomaly Detection using Isolation Forest
- Web dashboard with live graphs
- Alert system for suspicious activity

### Tech Stack
- Python 3.8+
- scikit-learn (Isolation Forest)
- Flask (web dashboard)
- psutil (system metrics)
- pandas, numpy

### Project Structure
```
Host Itrution System/
├── simple_dashboard.py    # Main web dashboard ← START HERE
├── main.py                # Full CLI interface
├── config.py              # Configuration
├── data_collector.py      # System metrics collection
├── feature_engineering.py # Feature extraction
├── ml_models.py           # Machine learning models
├── monitor.py             # Real-time monitoring engine
├── alert_system.py        # Alert management
├── requirements.txt       # Dependencies
└── templates/             # HTML dashboard templates
```

### Setup
```bash
pip install -r requirements.txt
python3 simple_dashboard.py
# Open: http://localhost:5000
```

### API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/status` | Current system status |
| GET | `/api/metrics` | Real-time metrics |
| GET | `/api/alerts` | Recent alerts |
| POST | `/api/start` | Start monitoring |
| POST | `/api/stop` | Stop monitoring |

### Configuration (`config.py`)
```python
MODEL_TYPE = 'isolation_forest'   # ML algorithm
CONTAMINATION = 0.1               # Expected anomaly ratio
COLLECTION_INTERVAL = 2           # Seconds between checks
ANOMALY_THRESHOLD = 0.6           # Detection sensitivity
```

---

## 3. Startup Idea Analyser

**Path:** `Startup idea analyser 2/`

An AI-powered **startup business analysis** workflow that generates a structured report evaluating a startup's health across financial, market, and strategic dimensions.

### Output Report Includes
- Startup overview & problem/solution summary
- Financial snapshot (revenue, expenses, profit margin)
- Startup score out of 100 (across 5 categories)
- SWOT analysis
- Competitive landscape review
- Marketing suggestions
- Growth strategy (short/mid/long-term)
- Risk analysis table
- Action plan

### Files
```
Startup idea analyser 2/
├── bussiness analyzer (1).json      # n8n workflow definition
└── startup_business_analysis_1.md  # Report template
```

---

## 4. Crop Disease Detection System

**Path:** `crop disease detection system/`

An AI-powered **plant disease detection** system. Users upload a crop image and receive a diagnosis of the disease along with treatment recommendations.

### Supported Crops (from sample reports)
- Tomato
- Potato
- Apple
- Grape

### Tech Stack
- FastAPI (REST API)
- Deep Learning model for image classification
- Interactive HTML frontend
- JSON diagnosis reports

### Project Structure
```
crop disease detection system/
├── api.py                # FastAPI application
├── model.py              # ML model definition
├── prediction_service.py # Inference service
├── config.py             # Configuration
├── frontend.html         # Basic frontend
├── frontend_interactive.html  # Interactive UI
├── web_server.py         # Web server
├── example_usage.py      # Usage examples
├── sample_diagnosis.py   # Sample diagnosis runner
├── text_diagnosis.py     # Text-based diagnosis
├── setup.sh              # Setup script
└── reports/              # Saved diagnosis JSON reports
```

### Setup
```bash
bash setup.sh
python api.py
```

---

## 5. Dental Clinic RAG

**Path:** `dental_clinic_rag/`

A **RAG (Retrieval-Augmented Generation) chatbot** for dental clinics. Upload clinic PDFs (procedures, FAQs, pricing) and ask natural language questions — the bot answers based only on your documents.

### Features
- Upload PDF documents via the sidebar
- AI-powered answers grounded in uploaded docs
- Source tracking (shows which document was used)
- Clean Django-based chat interface

### Tech Stack
| Layer | Technology |
|-------|------------|
| Web Framework | Django 4.2 |
| LLM | Google Gemini AI |
| PDF Processing | PyPDF2 |
| Text Retrieval | scikit-learn |

### Project Structure
```
dental_clinic_rag/
├── manage.py
├── dental_clinic_rag/         # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── rag_bot/                   # Main Django app
│   ├── models.py
│   ├── views.py
│   └── services/
│       ├── pdf_processor.py   # PDF text extraction
│       ├── gemini_service.py  # Gemini API integration
│       └── rag_service.py     # RAG retrieval logic
├── templates/rag_bot/chat.html
├── static/
│   ├── css/style.css
│   └── js/chat.js
├── requirements.txt
└── setup.sh
```

### Setup
```bash
# 1. Run setup
bash setup.sh

# 2. Add your Gemini API key to .env
GEMINI_API_KEY=your-key-here

# 3. Start server
python manage.py runserver
# Open: http://localhost:8000
```

---

## 6. Fake News Detector

**Path:** `fake news detector/`

A simple web tool that uses **Gemini AI** to analyze a news headline or article and classify it as True, Fake, or Misleading, with an explanation.

### Tech Stack
- Flask (backend API)
- Google Gemini AI (`gemini-2.5-flash-lite`)
- Vanilla HTML + CSS + JavaScript (frontend)

### Project Structure
```
fake news detector/
├── app.py        # Flask backend with Gemini integration
├── index.html    # Frontend UI
├── script.js     # Frontend logic
└── style.css     # Styling
```

### How It Works
1. User submits a news text via the web interface
2. Flask backend sends it to Gemini with a structured prompt
3. Gemini evaluates and returns: verdict (True/Fake/Misleading) + reasoning
4. Result is displayed in the browser

---

## 7. Folow — WhatsApp Follow-up System

**Path:** `folow/`

An **automated WhatsApp customer follow-up system** that sends scheduled WhatsApp messages to customers using FastAPI, Supabase (PostgreSQL), and n8n.

### Architecture
```
n8n Scheduler (Daily Cron)
       │
       ▼
FastAPI Backend (REST API)
       │
       ├──► Supabase (PostgreSQL) — stores customers
       │
       └──► WABIS API — sends WhatsApp messages
```

### n8n Workflow
```
Schedule Trigger → GET /today-followups → Split In Batches → POST WABIS API → PATCH /customer/{id}
```

### Tech Stack
| Layer | Technology |
|-------|------------|
| Backend | Python, FastAPI, SQLAlchemy |
| Database | Supabase (PostgreSQL) |
| Automation | n8n |
| WhatsApp | WABIS API |
| Frontend | React + Vite |

### Project Structure
```
folow/
├── backend/
│   ├── main.py           # FastAPI app & endpoints
│   ├── database.py       # SQLAlchemy connection
│   ├── models.py         # DB models
│   ├── requirements.txt
│   └── .env.example
├── frontend/             # React + Vite UI
│   └── src/App.jsx
├── supabase/
│   └── setup.sql         # DB schema
└── n8n_workflow/
    └── WhatsApp Followup Full Flow.json
```

### API Reference
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/customer` | Add a customer to the follow-up queue |
| GET | `/customers` | Get all customers |
| GET | `/today-followups` | Get today's pending follow-ups (used by n8n) |
| PATCH | `/customer/{id}` | Update customer status / retry count |

### Customer Status Values
| Status | Description |
|--------|-------------|
| `pending` | Waiting for follow-up |
| `processing` | Message being sent |
| `sent` | Delivered successfully |
| `failed` | Delivery failed |
| `returned` | Customer has returned/visited |

### Setup
```bash
# 1. Create Supabase project and run supabase/setup.sql
# 2. Configure backend
cd backend
pip install -r requirements.txt
cp .env.example .env
# Set DATABASE_URL in .env
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 3. Import n8n workflow and configure credentials
```

---

## 8. RAG Proto

**Path:** `rag_proto/`

A beginner-friendly **RAG (Retrieval-Augmented Generation) prototype** chatbot. Paste or upload text, then ask questions — the bot retrieves relevant sections and generates natural answers using Llama 3.2 via Ollama.

### How It Works
1. User provides context (paste text or upload a file)
2. Bot finds the most relevant section of that text
3. Llama 3.2 (via Ollama) reads the section and generates a natural answer

### Tech Stack
- Flask (web server)
- Ollama + Llama 3.2 (local LLM — free, runs offline)
- Simple HTML/CSS frontend

### Project Structure
```
rag_proto/
├── app.py              # Main Flask app + RAG logic
├── templates/
│   └── index.html      # Web interface
├── requirements.txt
└── setup.sh            # Ollama setup guide
```

### Setup
```bash
# 1. Install Ollama from https://ollama.com
# 2. Install dependencies
pip install -r requirements.txt
# 3. Run
python3 app.py
# Open: http://localhost:5000
# Llama 3.2 (~2GB) downloads automatically on first use
```

---

## 9. Rai Predictor — Kerala Rain Predictor

**Path:** `rai predictor/`

An AI-powered **rain prediction web app** trained on Kerala monsoon patterns. Users input weather parameters and get a rain probability prediction.

### Features
- Random Forest classifier (~85–90% accuracy)
- Accounts for Kerala's monsoon seasons (SW, NE, dry)
- Mobile-responsive web interface
- REST API endpoint

### Input Parameters
- Month (monsoon season awareness)
- Temperature
- Humidity
- Atmospheric Pressure
- Wind Speed

### Tech Stack
- Flask (web app)
- scikit-learn (Random Forest)
- pandas, numpy
- Synthetic dataset (1000 samples based on real Kerala patterns)

### Project Structure
```
rai predictor/
├── app.py               # Flask web application
├── train_model.py       # Model training script
├── rainfall_data.csv    # Training dataset (auto-generated)
├── requirements.txt
└── templates/
    └── index.html       # Web UI
```

### Setup
```bash
pip install -r requirements.txt
python train_model.py      # Train the model
python app.py              # Start the app
# Open: http://localhost:5000
```

### API Endpoint
```bash
POST http://localhost:5000/api/predict
Content-Type: application/json

{
    "month": 7,
    "temperature": 28.5,
    "humidity": 85,
    "pressure": 995,
    "wind_speed": 20
}
```

---

## 10. Simple CRM — SalesCRM

**Path:** `simple_crm/`

A lightweight **B2B Sales CRM** built with React, using Google Sheets as a live database via Google Apps Script.

### Features
- Leads Management — Add/edit/delete leads with status pipeline (New → Qualified → Proposal → Won/Lost)
- Deal Pipeline — Kanban board with drag-and-drop
- Activity Log — Timeline of calls, emails, meetings
- Reminders — Follow-ups grouped by Overdue / Today / Upcoming

### Tech Stack
| Layer | Technology |
|-------|------------|
| Frontend | React (Vite) |
| Backend | Google Apps Script |
| Database | Google Sheets |

### Google Sheets Structure
| Tab | Columns |
|-----|---------|
| Leads | id, name, company, email, phone, source, status, created_at |
| Deals | id, lead_id, title, value, stage, close_date, created_at |
| ActivityLog | id, lead_id, type, note, created_at |
| Reminders | id, lead_id, due_date, priority, note, done |

### Project Structure
```
simple_crm/
├── src/
│   └── App.jsx          # Main React CRM application
├── crm/                 # Backend logic
├── public/
├── index.html
├── vite.config.js
├── package.json
└── README.md
```

### Setup
1. Create a Google Sheet named **SalesCRM** with the 4 tabs above
2. Open **Extensions → Apps Script** and deploy as a Web App
3. Copy the Web App URL
4. In the React app, go to **Settings** and paste the URL

### Roadmap
- FastAPI + Supabase backend (production upgrade)
- CSV import for bulk lead upload
- Role-based access (Admin / Sales Rep)
- Dashboard charts (deal value by stage, leads by source)

---

## 11. Voice Assistant — JarvisNova

**Path:** `voice assistat/`

A browser-based **AI voice assistant** called JarvisNova. Listens via microphone, processes speech, and responds with voice + text in a real-time web UI.

### Capabilities
- Speech recognition (microphone input)
- Text-to-speech responses
- Time & date queries
- Open/close applications
- Web browsing
- Mood detection
- Persistent memory (saves user name)
- Reminders
- Custom commands

### Tech Stack
- Flask + Flask-SocketIO (real-time web server)
- Python `speech_recognition` library
- Custom TTS via `edge.py` / `speaker.py`
- Gemini / LLM API integration (`api.py`)
- Real-time UI (HTML + CSS + WebSocket)

### Project Structure
```
voice assistat/
├── main/
│   ├── main.py           # Flask + SocketIO server + main loop
│   ├── api.py            # LLM API integration
│   ├── app.py            # App launcher
│   ├── commands.py       # App open/close commands
│   ├── custom.py         # Custom command handling
│   ├── edge.py           # Edge TTS integration
│   ├── memory.py         # Name/memory persistence
│   ├── mood.py           # Mood detection
│   ├── nova.py           # Core assistant logic
│   ├── reminder.py       # Reminder management
│   ├── speaker.py        # Speech output
│   ├── time_date.py      # Date/time utilities
│   ├── wake_up.py        # Wake word detection
│   ├── web.py            # Web browsing commands
│   ├── index.html        # Frontend UI
│   └── static/
│       ├── script.js
│       └── style.css
└── speech/
    └── speaker.py
```

### Setup
```bash
pip install flask flask-socketio speechrecognition
python main/main.py
# Open the browser UI and speak to JarvisNova
```

---

## 🛠️ Common Requirements

Most projects require **Python 3.8+** and use a combination of:

```
flask / fastapi / django    # Web frameworks
scikit-learn                # Machine learning
pandas / numpy              # Data processing
google-generativeai         # Gemini AI
streamlit                   # Data apps
psutil                      # System monitoring
```

---

## 📄 License

All projects are under the **MIT License** — free to use, modify, and distribute.

---

*README generated from repository structure and source code at [arshad49/project_1.0](https://github.com/arshad49/project_1.0/tree/main/project)*
