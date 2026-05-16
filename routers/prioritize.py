from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from groq import Groq
import os
import json
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


class PrioritizeRequest(BaseModel):
    tasks: list[dict]


class PrioritizeResponse(BaseModel):
    suggestions: list[dict]


@router.post("", response_model=PrioritizeResponse)
def prioritize_tasks(body: PrioritizeRequest):
    task_list = "\n".join(
        f"- id: {t.get('id')}, title: {t.get('title')}, current priority: {t.get('priority', 'N/A')}, due: {t.get('dueDate', 'none')}"
        for t in body.tasks
    )

    prompt = (
        "You are a project manager assistant. Given the following tasks, suggest a priority "
        "(HIGH, MEDIUM, or LOW) for each one. Return a JSON array only, no explanation.\n"
        'Format: [{"id": "<task_id>", "suggestedPriority": "HIGH|MEDIUM|LOW", "reason": "<short reason>"}]\n\n'
        f"Tasks:\n{task_list}"
    )

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
        )
        raw = response.choices[0].message.content.strip()
        # Extract JSON array from response
        start = raw.find("[")
        end = raw.rfind("]") + 1
        suggestions = json.loads(raw[start:end])
        return PrioritizeResponse(suggestions=suggestions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
