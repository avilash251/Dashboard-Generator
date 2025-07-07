# backend/routes/chat.py
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from agents.crew_routes import handle_prompt_with_crew
from utils.slm_router import slm_respond
from utils.predict_next import generate_followup
from dbscripts.audit_db import save_log

router = APIRouter()

@router.post("/api/chat")
async def chat(request: Request):
    try:
        body = await request.json()
        user_prompt = body.get("prompt", "").strip()

        # Step 1: Save initial prompt from user
        await save_log(user_prompt, source="user")

        # Step 2: Instant SLM response (e.g., "Thanks, generating...")
        slm_response = slm_respond(user_prompt)
        if slm_response:
            return {
                "slm": slm_response,
                "layout": [],
                "next": []
            }

        # Step 3: Run CrewAI agents for full layout generation
        result = handle_prompt_with_crew(user_prompt)
        charts = result.get("charts", [])
        raw_output = result.get("raw", "")
        followups = result.get("followups", [])

        # Step 4: Save the crewAI output to audit log
        await save_log(user_prompt, source="CrewAI", response=str(raw_output))

        # Step 5: Predict follow-up suggestions
        next_suggestions = generate_followup(user_prompt)

        return {
            "slm": None,
            "layout": charts,
            "next": next_suggestions
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
