# import os
# import json
# from fastapi import APIRouter, Request
# from utils.db_logger import get_prompt_trend
# from ws.socketio_server import emit_metric_update
# import google.generativeai as genai

# router = APIRouter()

# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# @router.post("/api/chat")
# async def generate_followup(request: Request):
#     data = await request.json()
#     user_prompt = data.get("prompt", "")

#     try:
#         # Construct prompt chaining logic
#         full_prompt = f"""
# You are an expert Prometheus agent.

# The user asked:
# "{user_prompt}"

# Please suggest 5 intelligent next queries related to this topic.
# Respond as a JSON list.
# """

#         model = genai.GenerativeModel("gemini-1.5-flash")
#         response = model.generate_content(full_prompt)
#         text = response.text.strip()

#         # Try to safely extract JSON
#         if not text.startswith("["):
#             text = "[" + text.split("[", 1)[-1]
#         suggestions = json.loads(text)

#         # Save prompt + response to DB
#         await get_prompt_trend(user_prompt, suggestions)

#         # Notify clients to refresh prompt trend
#         await emit_metric_update()

#         return {"suggestions": suggestions}

#     except Exception as e:
#         print("[Gemini Error]", e)
#         return {"suggestions": ["Unable to generate follow-ups"]}

# from agents.crew_routes import handle_prompt_with_crew

# def generate_followup(prompt: str) -> list:
#     return handle_prompt_with_crew(prompt)

# backend/utils/predict_next.py

from rapidfuzz import fuzz

# 🔸 Sample follow-up prompts for key intents
FOLLOWUP_MAP = {
    "cpu_usage": [
        "Show CPU usage for all nodes",
        "Compare CPU usage across time",
        "Alert if CPU crosses 80%"
    ],
    "memory_usage": [
        "Show memory usage trend",
        "Alert for high memory usage",
        "Compare heap and buffer usage"
    ],
    "disk_info": [
        "Show disk usage for each volume",
        "Disk I/O trend over 6h",
        "Trigger alert if disk < 10% free"
    ],
    "uptime_status": [
        "Show uptime for all servers",
        "Detect recent restarts",
        "Track node stability"
    ]
}

# 🔍 Intents and fallback logic
INTENT_KEYWORDS = {
    "cpu_usage": ["cpu", "processor", "core", "utilization"],
    "memory_usage": ["memory", "ram", "heap", "cache"],
    "disk_info": ["disk", "storage", "drive", "partition"],
    "uptime_status": ["uptime", "boot", "restarted", "start"]
}


def match_intent(prompt: str) -> str | None:
    prompt = prompt.lower()
    for intent, keywords in INTENT_KEYWORDS.items():
        for keyword in keywords:
            if fuzz.partial_ratio(keyword, prompt) > 75:
                return intent
    return None


def generate_followup(prompt: str) -> list[str]:
    intent = match_intent(prompt)
    if intent and intent in FOLLOWUP_MAP:
        return FOLLOWUP_MAP[intent]
    return ["Would you like to explore memory, CPU or disk metrics?", 
            "You can ask for latency, errors or trends next."]
