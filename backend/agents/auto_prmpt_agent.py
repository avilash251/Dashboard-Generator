from utils.slm_router import slm_respond
from utils.gemini_wrapper import ask_gemini

def generate_layout(prompt: str, time_range: str, prometheus_url: str):
    try:
    # Try small-language-model (SLM) first
        slm_result = slm_respond(prompt)
        if slm_result:
            return slm_result

        # Fallback to Gemini layout generation
        return ask_gemini(prompt, time_range, prometheus_url)
    except Exception as e:
        return f"auto prompt error: {str(e)}"

