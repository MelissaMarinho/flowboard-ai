# FlowBoard — AI Microservice

> FastAPI microservice providing AI-powered project summaries and task prioritisation via Groq's LLM API.

[![CI](https://github.com/marinhomelissa65/flowboard-ai/actions/workflows/ci.yml/badge.svg)](https://github.com/marinhomelissa65/flowboard-ai/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat-square&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![Groq](https://img.shields.io/badge/Groq-LLaMA_3.1-F55036?style=flat-square)](https://console.groq.com)
[![Render](https://img.shields.io/badge/deployed_on-Render-46E3B7?style=flat-square)](https://render.com)

---

## Architecture

```
flowboard-web (Next.js on Vercel)
        │
        │  POST /summarize
        │  POST /prioritize
        ▼
┌──────────────────────────┐
│   FastAPI Microservice   │
│   Python 3.12 · Uvicorn  │
│   Deployed on Render     │
└────────────┬─────────────┘
             │ Groq SDK
             ▼
      Groq API (free tier)
      llama-3.1-8b-instant
```

---

## Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Health check — returns `{ "status": "ok" }` |
| `POST` | `/summarize` | Generate a natural-language summary of a project's tasks |
| `POST` | `/prioritize` | Suggest HIGH / MEDIUM / LOW priorities for a list of tasks |

### POST /summarize

**Request**
```json
{
  "project_name": "My Project",
  "tasks": [
    { "id": "1", "title": "Set up CI", "status": "DONE", "priority": "HIGH" },
    { "id": "2", "title": "Write tests", "status": "IN_PROGRESS", "priority": "MEDIUM" }
  ]
}
```

**Response**
```json
{
  "summary": "My Project is progressing well with 1 task completed and 1 in progress..."
}
```

### POST /prioritize

**Request**
```json
{
  "tasks": [
    { "id": "1", "title": "Fix auth bug", "priority": "MEDIUM", "dueDate": "2025-06-01" }
  ]
}
```

**Response**
```json
{
  "suggestions": [
    {
      "id": "1",
      "suggestedPriority": "HIGH",
      "reason": "Auth issues block all users and should be resolved immediately."
    }
  ]
}
```

---

## Local Development

### Setup

```bash
# 1. Clone and create a virtual environment
git clone https://github.com/marinhomelissa65/flowboard-ai.git
cd flowboard-ai
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Add your GROQ_API_KEY — get a free key at https://console.groq.com
```

### Run

```bash
uvicorn main:app --reload
```

- API: [http://localhost:8000](http://localhost:8000)
- Interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs)

Or use the Makefile shortcut:

```bash
make dev
```

---

## Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | API key from [console.groq.com](https://console.groq.com) — free tier available |

---

## Deployment (Render — free tier)

1. Push this repo to GitHub
2. Create a new **Web Service** on [render.com](https://render.com)
3. Connect the repo — Render picks up `render.yaml` automatically
4. Add `GROQ_API_KEY` as an environment variable in the Render dashboard
5. Every push to `main` triggers an automatic redeploy

> **Note:** Render's free tier spins down after 15 minutes of inactivity. The first request after idle may take ~30 seconds to warm up.

---

## Project Structure

```
flowboard-ai/
├── main.py               # FastAPI app, CORS middleware, router registration
├── routers/
│   ├── summarize.py      # POST /summarize — project summary via Groq
│   └── prioritize.py     # POST /prioritize — task priority suggestions
├── requirements.txt      # Pinned dependencies
├── .python-version       # Pins Python 3.12 for Render
├── render.yaml           # Render deployment config
├── Makefile              # Dev shortcuts
└── .env.example          # Environment variable template
```

---

## Related

- **[flowboard-web](https://github.com/marinhomelissa65/flowboard-web)** — Next.js frontend that consumes this service and renders the AI results
