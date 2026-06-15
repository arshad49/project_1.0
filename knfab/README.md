# SalesCRM

A lightweight, professional B2B Sales CRM built with React and Google Sheets as a live database via Google Apps Script.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React (Claude Artifact) |
| Backend | Google Apps Script |
| Database | Google Sheets |
| Hosting | Claude.ai Artifacts |

---

## Features

- **Leads Management** — Add, edit, delete leads with status tracking (New → Qualified → Proposal → Won / Lost)
- **Deal Pipeline** — Kanban board with drag-and-drop across stages, deal value tracking
- **Activity Log** — Timeline of calls, emails, and meetings per contact
- **Reminders** — Follow-up reminders grouped by Overdue / Today / Upcoming with mark-done
- **Settings** — Configure Apps Script URL, test connection, persisted in localStorage

---

## Project Structure

```
salescrm/
├── frontend/
│   └── CRM.jsx              # Single React component (all views)
├── backend/
│   └── appsscript.js        # Google Apps Script backend
├── docs/
│   └── sheets-setup.md      # Google Sheets tab + header setup guide
└── README.md
```

---

## Google Sheets Setup

Create a Google Sheet named **SalesCRM** with these 4 tabs and exact headers:

**Leads**
```
id | name | company | email | phone | source | status | created_at
```

**Deals**
```
id | lead_id | title | value | stage | close_date | created_at
```

**ActivityLog**
```
id | lead_id | type | note | created_at
```

**Reminders**
```
id | lead_id | due_date | priority | note | done
```

---

## Backend Setup (Google Apps Script)

1. Open your Google Sheet → **Extensions → Apps Script**
2. Paste the contents of `backend/appsscript.js`
3. Click **Deploy → New Deployment**
   - Type: **Web App**
   - Execute as: **Me**
   - Who has access: **Anyone**
4. Copy the generated **Web App URL**

### API Reference

| Method | Usage |
|---|---|
| `GET ?sheet=Leads` | Fetch all rows from a tab |
| `POST { sheet, action: "insert", row }` | Append a new row |
| `POST { sheet, action: "update", id, row }` | Update a row by id |
| `POST { sheet, action: "delete", id }` | Delete a row by id |

---

## Frontend Setup

1. Open the CRM in Claude Artifacts
2. Navigate to **Settings**
3. Paste your Apps Script Web App URL
4. Click **Save** then **Test Connection**
5. Green dot in sidebar = connected and ready

---

## Roadmap

- [ ] FastAPI + Supabase backend (production upgrade)
- [ ] Google Sheets two-way sync
- [ ] Email notifications for overdue reminders
- [ ] CSV import for bulk lead upload
- [ ] Role-based access (Admin / Sales Rep)
- [ ] Dashboard charts (deal value by stage, leads by source)

---

## Local Development

No local setup needed. The frontend runs entirely inside Claude Artifacts. The backend runs on Google's infrastructure via Apps Script.

For the production upgrade (FastAPI + Supabase):

```bash
git clone https://github.com/yourname/salescrm
cd salescrm/backend-api
pip install -r requirements.txt
cp .env.example .env   # fill in Supabase + Sheets credentials
uvicorn main:app --reload
```

---

## Environment Variables (Production)

```
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
GOOGLE_SHEET_ID=your_sheet_id
GOOGLE_CREDENTIALS_JSON=path/to/service_account.json
```

---

## Contributing

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m "add: your feature"`
4. Push and open a Pull Request

---

## License

MIT — free to use, modify, and distribute.
