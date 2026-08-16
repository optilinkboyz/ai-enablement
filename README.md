# AI Enablement Starter Kit

> A lightweight AI assistant that lets **non-technical employees** understand documents, get answers, and summarise content — with no technical knowledge required.

Built as a **Proof of Concept (PoC)** for your organisation — Digital & AI Enablement.

---

## What Problem Does This Solve?

AI tools are powerful — but most require technical knowledge to use effectively. This creates a gap where only IT and data teams benefit from AI, while HR, Finance, Operations, and Procurement staff are left out.

**This kit closes that gap.** It provides:
1. **A simple web tool** — upload a document, ask a question, get a plain-language answer
2. **An enablement package** — user guide, best practices, and a demo script so any team lead can introduce it to their department

---

## Features

| Feature | Description |
|---|---|
| Document Upload | PDF, DOCX, and TXT files up to 10MB |
| Q&A | Ask questions about uploaded documents or general topics |
| Summarisation | Short, medium, or detailed summaries |
| Model Fallback | Automatically switches AI models if one is busy |
| Clean UI | your organisation-branded, mobile-responsive, no training required |
| No Storage | Documents processed in memory — never saved |

---

## Architecture
**Tech stack:** React 18 · Python 3.12 · FastAPI · Google Gemini API · PyPDF2 · python-docx

---

## Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env   # add your GEMINI_API_KEY
python main.py         # http://localhost:8000/docs
```

### Frontend
```bash
cd frontend
npm install
npm start              # http://localhost:3000
```

---

## Project Structure
---

## Enablement Package

| Document | Audience | Purpose |
|---|---|---|
| [User Guide](docs/user-guide.md) | All employees | How to use the tool |
| [Best Practices](docs/best-practices.md) | Employees + team leads | Responsible use, data handling |
| [Demo Script](docs/demo-script.md) | Team leads / IT | 10-minute team demo |

---

## API Reference

| Endpoint | Method | Description |
|---|---|---|
| `/health` | GET | System status |
| `/upload` | POST | Upload document → extracted text |
| `/ask` | POST | Ask a question |
| `/summarise` | POST | Summarise document |

---

## Author

**Andrew Nelson Enoh** — MSc Industrial Data Science, Montanuniversität Leoben
[GitHub](https://github.com/optilinkboyz) · nelsonenoh@gmail.com

*Independent PoC — not an official your organisation product.*
