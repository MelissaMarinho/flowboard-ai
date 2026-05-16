# FlowBoard — AI Microservice

FastAPI microservice that provides AI-powered project summaries and task prioritisation using Groq's free LLM API.

## Architecture

```
flowboard-web (Next.js)
        │
        │ POST /summarize
        │ POST /prioritize
        ▼
┌───────────────────────────┐
│   FastAPI Microservice    │
│   Python · Uvicorn        │
│   Deployed on Render      │
│   (free tier)             │
└────────────┬──────────────┘
             │
             ▼
      Groq API (free tier)
      llama-3.1-8b-instant
```

## Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/summarize` | Generate a natural language summary of a project's tasks |
| `POST` | `/prioritize` | Suggest priority levels for a list of tasks |

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
  "summary": "My Project is progressing well with 1 task completed and 1 currently in progress..."
}
```

### POST /prioritize

**Request**
```json
{
  "tasks": [
    { "id": "1", "title": "Fix auth bug", "priority": "MEDIUM", "dueDate": "2024-12-01" }
  ]
}
```

**Response**
```json
{
  "suggestions": [
    { "id": "1", "suggestedPriority": "HIGH", "reason": "Auth bugs block all users" }
  ]
}
```

## Getting Started

### 1. Clone and set up

```bash
git clone https://github.com/your-username/flowboard-ai.git
cd flowboard-ai
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment variables

```bash
cp .env.example .env
```

Add your Groq API key to `.env` — get a free key at [console.groq.com](https://console.groq.com).

### 3. Run locally

```bash
uvicorn main:app --reload
```

API is available at [http://localhost:8000](http://localhost:8000).  
Interactive docs at [http://localhost:8000/docs](http://localhost:8000/docs).

## Deployment (Render — free)

1. Push this repo to GitHub
2. Create a new **Web Service** on [render.com](https://render.com)
3. Connect the repo — Render auto-detects `render.yaml`
4. Add `GROQ_API_KEY` as an environment variable
5. Deploy — Render auto-deploys on every push to `main`

> **Note:** Render free tier spins down after 15 minutes of inactivity. The first request after idle may take ~30 seconds.

## Project Structure

```
flowboard-ai/
├── main.py               # FastAPI app, CORS, router registration
├── routers/
│   ├── summarize.py      # POST /summarize — project summary via Groq
│   └── prioritize.py     # POST /prioritize — task priority suggestions
├── requirements.txt
├── render.yaml           # Render deployment config
└── .env.example
```

## Related

- **[flowboard-web](https://github.com/your-username/flowboard-web)** — Next.js frontend that consumes this service
