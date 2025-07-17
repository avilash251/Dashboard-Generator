from datetime import datetime
from utils.prompt_utils import is_pure_greeting, is_greeting, sanitize_prompt

# ✅ Entry point for SLM logic
def handle_slm_response(prompt: str):
    prompt = prompt.strip()
    
    # Pure greeting? Return early, no LLM
    if is_pure_greeting(prompt):
        return {
            "summary": "Hello! How can I assist you?",
            "layout": {},
            "meta": {
                "timestamp": datetime.utcnow().isoformat(),
                "context_role": "greeting",
                "context_scope": "none",
                "source": "slm"
            },
            "next": [
                "CPU usage of host1",
                "Memory stats by pod",
                "Check alerts for namespace=prod"
            ]
        }

    # Otherwise: clean prompt + return greeting string
    cleaned = sanitize_prompt(prompt)
    greeting = "Hi there 👋! Let me get that for you..." if is_greeting(prompt) else None

    return {
        "greeting_msg": greeting,
        "cleaned_prompt": cleaned
    }
