from fastapi import APIRouter, Request
from utils.slm_router import slm_respond
from utils.predict_next import generate_followup
from utils.gemini_wrapper import ask_gemini
from routes.history import save_audit_log

chat_router = APIRouter()

@chat_router.post("/chat")
async def chat(request: Request):
    try:
        body = await request.json()
        user_prompt = body.get("prompt", "")
        await save_audit_log(user_prompt, source="user")

        slm_response = slm_respond(user_prompt)
        if slm_response:
            return {"slm": slm_response, "layout": [], "next": []}

        gemini_layout = ask_gemini(user_prompt)
        next_suggestions = generate_followup(user_prompt)

        return {
            "slm": None,
            "layout": gemini_layout,
            "next": next_suggestions
        }
    except Exception as e:
        return {"error": str(e)}
