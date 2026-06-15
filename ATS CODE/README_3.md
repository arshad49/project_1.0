# 📄 Resume Ranker — ATS Tool

A lightweight **Applicant Tracking System (ATS)** built with Python and Streamlit. Upload multiple resumes and paste a job description — the app ranks candidates by relevance using **TF-IDF** and **cosine similarity**.

---

## ✨ Features

- 📋 Paste any job description as input
- 📂 Upload multiple PDF resumes at once
- 🤖 Ranks resumes by match score using TF-IDF vectorization
- 📊 Displays results in a sorted table (best match first)

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/resume-ranker.git
cd resume-ranker
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run ats.py
```

The app will open at `http://localhost:8501`

---

## 📦 Requirements

```
streamlit
pandas
pypdf
scikit-learn
```

> Save as `requirements.txt` and install with `pip install -r requirements.txt`

---

## 🧠 How It Works

1. The job description and all uploaded resumes are extracted as plain text
2. All documents are vectorized together using **TF-IDF** (Term Frequency–Inverse Document Frequency)
3. **Cosine similarity** is computed between the job description vector and each resume vector
4. Resumes are ranked and displayed from highest to lowest match score

---

## 📁 Project Structure

```
resume-ranker/
├── ats.py             # Main Streamlit application
└── requirements.txt   # Python dependencies
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Streamlit |
| PDF Parsing | pypdf |
| ML / Ranking | scikit-learn (TF-IDF + Cosine Similarity) |
| Data Display | pandas |

---

## 📄 License

MIT
