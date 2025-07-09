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

from utils.intent_detector import detect_intent
from utils.gemini_wrapper import ask_gemini

# 🔗 Prompt chaining logic
def handle_prompt_with_crew(prompt: str) -> list:
    intent = detect_intent(prompt)

    # 🔒 Handle malicious or unknown
    if "Sorry" in intent:
        return [intent]

    # 🧠 Use prompt chaining based on known intent
    intent_chains = {
        "cpu_usage": [
            "Show CPU usage for server1",
            "What is the max CPU over the last 6 hours?",
            "Compare CPU across nodes"
        ],
        "memory_usage": [
            "Current memory usage trend",
            "Compare memory vs cache usage",
            "Memory swap rate on node2"
        ],
        "disk_info": [
            "Disk space left on root partition",
            "Which volume is almost full?",
            "Show inode usage for /data"
        ],
        "error_rate": [
            "HTTP 5xx error trend",
            "Error rates by namespace",
            "Spike in failed logins?"
        ]
        # Add more intent suggestions here...
    }

    if intent in intent_chains:
        return intent_chains[intent]

    # 🤖 Fallback to Gemini for less common prompts
    try:
        gemini_resp = ask_gemini(f"What follow-up questions would you recommend for: {prompt}?")
        return gemini_resp.split("\n") if gemini_resp else ["No suggestions found."]
    except Exception as e:
        return [f"Gemini error: {str(e)}"]

