from typing import Optional

def slm_respond(prompt: str) -> Optional[str]:

    """
    Lightweight rule-based prompt router for simple interactions.
    Returns a response if the prompt is simple (greeting, thanks, help), or None to fallback.
    """

    prompt_lower = prompt.strip().lower()

    # Greeting and small talk
    if any(word in prompt_lower for word in ["hello", "hi", "hey", "good morning", "good evening"]):
        return "👋 Hello! How can I assist you with your metrics or dashboard today?"

    # Gratitude
    if "thank" in prompt_lower:
        return "🙏 You're welcome! Let me know if there's anything else you need."

    # Help / guidance
    if "help" in prompt_lower or "how to" in prompt_lower or "usage" in prompt_lower:
        return (
            "🧠 I can assist you with:\n"
            "- Creating Prometheus dashboards\n"
            "- Generating PromQL queries\n"
            "- Showing server health metrics\n"
            "- Explaining infrastructure KPIs\n"
            "Just type something like: 'Show me server1 analysis'."
        )

    # Fallback: prompt not understood by SLM
    return None
