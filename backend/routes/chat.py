from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from utils.gemini_wrapper import ask_gemini
from utils.slm_router import slm_respond
from agents.auto_prmpt_agent import generate_layout  # ⬅️ New import

router = APIRouter()

class ChatRequest(BaseModel):
    prompt: str
    time_range: str = "1h"
    prometheus_url: str = "http://localhost:9090"

@router.post("/chat")
def chat_with_agent(req: ChatRequest):
    try:
        layout = generate_layout(req.prompt, req.time_range, req.prometheus_url)
        return {"response": layout}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat handling failed: {str(e)}")
