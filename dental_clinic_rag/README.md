# Dental Clinic RAG Bot

Simple AI chatbot for dental clinics using Django and Gemini AI.

## Features

- Upload PDF documents
- AI-powered answers based on your documents
- Clean chat interface
- Source tracking

## Setup

### 1. Install Dependencies

```bash
./setup.sh
```

### 2. Add Gemini API Key

Get API key: https://aistudio.google.com/app/apikey

Edit `.env`:
```bash
GEMINI_API_KEY=your-key-here
```

### 3. Run Server

```bash
python manage.py runserver
```

Visit: http://localhost:8000

## Usage

1. Upload PDF documents in the sidebar
2. Ask questions in the chat
3. Get answers based on your documents

## Project Structure

```
dental_clinic_rag/
├── rag_bot/              # Main app
│   ├── models.py        # Database models
│   ├── views.py         # HTTP handlers
│   └── services/        # Business logic
│       ├── pdf_processor.py
│       ├── gemini_service.py
│       └── rag_service.py
├── templates/           # HTML templates
├── static/             # CSS/JS files
└── requirements.txt    # Dependencies
```

## Tech Stack

- Django - Web framework
- Gemini AI - Language model
- PyPDF2 - PDF processing
- scikit-learn - Text retrieval

## License

MIT
