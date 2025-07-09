# backend/routes/chat.py

from fastapi import APIRouter, Request
from utils.intent_detector import IntentDetector
from utils.content_classifier import infer_context_role, infer_context_scope
from utils.rag_context import retrieve_context
from utils.gemini_wrapper import ask_gemini
from utils.predict_next import generate_followup
from utils.slm_router import slm_respond
from routes.history import save_audit_log

chat_router = APIRouter()
intent_detector = IntentDetector()

@chat_router.post("/chat")
async def chat(request: Request):
    try:
        body = await request.json()
        user_prompt = body.get("prompt", "").strip()

        await save_audit_log(user_prompt, source="user")

        # First, try SLM fallback (for greetings)
        slm_response = slm_respond(user_prompt)
        if slm_response:
            return {
                "slm": slm_response,
                "layout": [],
                "next": [],
                "context_role": "Greeter",
                "context_scope": "greeting"
            }

        # Step 1: Intent detection
        intent = intent_detector.predict(user_prompt)

        # Step 2: Context classification
        context_role = infer_context_role(user_prompt)
        context_scope = infer_context_scope(user_prompt)

        # Step 3: RAG-enhanced Gemini layout generation
        context = retrieve_context(user_prompt)
        layout = ask_gemini(user_prompt, context)

        # Step 4: Predict follow-up prompts
        next_prompts = generate_followup(user_prompt)

        # Step 5: Save to audit log (enriched)
        await save_audit_log(user_prompt, source="system", metadata={
            "intent": intent,
            "context_role": context_role,
            "context_scope": context_scope
        })

        return {
            "slm": None,
            "layout": layout,
            "next": next_prompts,
            "context_role": context_role,
            "context_scope": context_scope
        }

    except Exception as e:
        return {"error": str(e)}
