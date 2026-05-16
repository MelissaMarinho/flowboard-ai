from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


class SummarizeRequest(BaseModel):
    project_name: str
    tasks: list[dict]


class SummarizeResponse(BaseModel):
    summary: str


@router.post("", response_model=SummarizeResponse)
def summarize_project(body: SummarizeRequest):
    todo = [t for t in body.tasks if t.get("status") == "TODO"]
    in_progress = [t for t in body.tasks if t.get("status") == "IN_PROGRESS"]
    done = [t for t in body.tasks if t.get("status") == "DONE"]

    task_breakdown = (
        f"To Do: {len(todo)}, In Progress: {len(in_progress)}, Done: {len(done)}.\n"
    )
    task_titles = "\n".join(
        f"- [{t.get('status')}] {t.get('title')} (priority: {t.get('priority', 'N/A')})"
        for t in body.tasks
    )

    prompt = (
        f"You are a project manager assistant. Summarise the current state of the project "
        f'"{body.project_name}" in 2-3 sentences.\n\n'
        f"{task_breakdown}\nTasks:\n{task_titles}"
    )

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
        )
        return SummarizeResponse(summary=response.choices[0].message.content.strip())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
