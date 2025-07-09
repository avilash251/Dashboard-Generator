# backend/routes/chat.py
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from utils.intent_detector import detect_intent
from utils.predict_next import handle_prompt_with_crew
from utils.gemini_wrapper import ask_gemini
from dbscripts.audit_db import save_log

router = APIRouter()

@router.post("/api/chat")
async def chat(request: Request):
    try:
        body = await request.json()
        user_prompt = body.get("prompt", "")
        
        intent = detect_intent(user_prompt)

        # Handle blocked/suspicious
        if intent.startswith("Sorry"):
            await save_log(user_prompt, source="user", flagged=True)
            return {"slm": intent, "layout": [], "next": []}

        if intent.startswith("Did you mean"):
            await save_log(user_prompt, source="user", flagged=True)
            return {"slm": intent, "layout": [], "next": []}

        await save_log(user_prompt, source="user", flagged=False)

        layout = ask_gemini(user_prompt)
        suggestions = handle_prompt_with_crew(user_prompt)

        return {
            "slm": None,
            "layout": layout,
            "next": suggestions
        }


    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
