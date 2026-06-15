# 📲 WhatsApp Customer Follow-up System

An automated WhatsApp follow-up system built with **FastAPI**, **Supabase (PostgreSQL)**, and **n8n** — sends scheduled WhatsApp messages to customers using the WABIS API.

---

## 🏗️ Architecture Overview

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  n8n Scheduler  │────▶│  FastAPI Backend  │────▶│  Supabase (PG)  │
│  (Daily Cron)   │     │  (REST API)       │     │  (Database)     │
└─────────────────┘     └──────────────────┘     └─────────────────┘
         │                                                  
         ▼                                                  
┌─────────────────┐                                         
│   WABIS API     │                                         
│ (WhatsApp msgs) │                                         
└─────────────────┘
```

**n8n Workflow:** `Schedule Trigger → GET /today-followups → Split In Batches → Send WhatsApp → PATCH /customer/{id}`

---

## 📁 Project Structure

```
folow/
├── backend/
│   ├── .env.example          # Environment variable template
│   ├── requirements.txt      # Python dependencies
│   ├── main.py               # FastAPI application & endpoints
│   ├── database.py           # SQLAlchemy database connection
│   └── models.py             # Database models
└── supabase/
    └── setup.sql             # Database setup script
```

---

## 🚀 Setup Instructions

### 1. Setup Supabase Database

1. Create a project at [supabase.com](https://supabase.com)
2. Open the **SQL Editor**
3. Run the contents of `supabase/setup.sql`
4. Go to **Project Settings → Database** and copy your connection string

### 2. Setup Backend

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and set your DATABASE_URL:
# DATABASE_URL=postgresql://postgres.[project-id]:[password]@aws-0-[region].pooler.supabase.com:5432/postgres
```

### 3. Run the Server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

| Interface | URL |
|-----------|-----|
| API | http://localhost:8000 |
| Swagger Docs | http://localhost:8000/docs |
| ReDoc | http://localhost:8000/redoc |

---

## 📡 API Reference

### `POST /customer`
Add a new customer to the follow-up queue.

```json
{
  "name": "John Doe",
  "phone": "9876543210",
  "last_visit": "2024-01-15",
  "next_followup": "2024-01-22",
  "template_name": "follow_up_basic"
}
```

### `GET /customers`
Returns all customers.

### `GET /today-followups`
Returns customers whose `next_followup` is today and whose status is `pending`. Used by the n8n scheduler.

### `PATCH /customer/{id}`
Update a customer's status or retry count.

```json
{
  "status": "sent",
  "retry_count": 0
}
```

---

## 🔧 Reference Values

### Valid `template_name` Values

| Value | Description |
|-------|-------------|
| `follow_up_basic` | Standard follow-up message |
| `festival_offer` | Seasonal/festival promotion |
| `discount_offer` | Discount campaign |

### Valid `status` Values

| Status | Description |
|--------|-------------|
| `pending` | Customer added, waiting for follow-up |
| `processing` | WhatsApp message being sent via n8n |
| `sent` | Message delivered successfully |
| `failed` | Message delivery failed |
| `returned` | Customer has visited/returned |

---

## ⚙️ n8n Workflow

The included n8n workflow (`WhatsApp_Followup_Full_Flow.json`) automates the full follow-up cycle:

```
Schedule Trigger (Daily)
       │
       ▼
GET /today-followups
       │
       ▼
Split In Batches (1 at a time)
       │
       ▼
POST WABIS API (Send WhatsApp template)
       │
       ▼
PATCH /customer/{id}  →  status: "sent"
```

**Import steps:**
1. Open your n8n instance
2. Go to **Workflows → Import**
3. Upload `WhatsApp_Followup_Full_Flow.json`
4. Update credentials (WABIS API token, phone number ID, template ID)
5. Update the backend URL (replace ngrok URL with your server)
6. Activate the workflow

**Retry logic (recommended enhancement):**
- Only retry if `retry_count < 3`
- On failure: PATCH status to `failed` and increment `retry_count`

---

## 🔑 Environment Variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | Supabase PostgreSQL connection string |

---

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI, SQLAlchemy
- **Database:** Supabase (PostgreSQL)
- **Automation:** n8n
- **WhatsApp:** [WABIS API](https://wabis.in)

---

## 📄 License

MIT
