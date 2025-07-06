from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agents.auto_prompt_agent import generate_layout

router = APIRouter()

class LayoutRequest(BaseModel):
    prompt: str

@router.post("/layout")
def get_layout(req: LayoutRequest):
    try:
        layout = generate_layout(req.prompt)
        return layout
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Layout generation failed: {str(e)}")
