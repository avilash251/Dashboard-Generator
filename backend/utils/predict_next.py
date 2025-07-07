import os
import json
from fastapi import APIRouter, Request
from utils.db_logger import get_prompt_trend
from ws.socketio_server import notify_trend_update
import google.generativeai as genai

router = APIRouter()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@router.post("/api/chat")
async def generate_followup(request: Request):
    data = await request.json()
    user_prompt = data.get("prompt", "")

    try:
        # Construct prompt chaining logic
        full_prompt = f"""
You are an expert Prometheus agent.

The user asked:
"{user_prompt}"

Please suggest 5 intelligent next queries related to this topic.
Respond as a JSON list.
"""

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(full_prompt)
        text = response.text.strip()

        # Try to safely extract JSON
        if not text.startswith("["):
            text = "[" + text.split("[", 1)[-1]
        suggestions = json.loads(text)

        # Save prompt + response to DB
        await get_prompt_trend(user_prompt, suggestions)

        # Notify clients to refresh prompt trend
        await notify_trend_update()

        return {"suggestions": suggestions}

    except Exception as e:
        print("[Gemini Error]", e)
        return {"suggestions": ["Unable to generate follow-ups"]}
