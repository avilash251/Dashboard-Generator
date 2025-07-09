from fastapi import APIRouter, Request
from utils.slm_router import slm_respond
from utils.predict_next import handle_prompt_with_crew
from utils.gemini_wrapper import ask_gemini
from routes.history import save_audit_log
from utils.context_classifier import infer_context_role, infer_context_scope

chat_router = APIRouter()

@chat_router.post("/chat")
async def chat(request: Request):
    try:
        body = await request.json()
        user_prompt = body.get("prompt", "")
        await save_audit_log(user_prompt, source="user")

        slm_response = slm_respond(user_prompt)
        if slm_response:
            return {
                "slm": slm_response,
                "layout": [],
                "next": [],
                "context_role": "SLM",
                "context_scope": "narrow"
            }

        context_role = infer_context_role(user_prompt)
        context_scope = infer_context_scope(user_prompt)
        gemini_layout = ask_gemini(user_prompt)
        next_suggestions = handle_prompt_with_crew(user_prompt)

        return {
            "slm": None,
            "layout": gemini_layout,
            "next": next_suggestions,
            "context_role": context_role,
            "context_scope": context_scope
        }
    except Exception as e:
        return {"error": str(e)}
