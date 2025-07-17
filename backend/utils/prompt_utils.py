import re

def sanitize_prompt(prompt: str) -> str:
    prompt = prompt.lower().strip()

    # Remove polite prefixes
    remove_phrases = [
        "hi", "hello", "hey", "please", "can you", "could you",
        "would you", "show me", "give me", "tell me"
    ]

    for phrase in remove_phrases:
        if prompt.startswith(phrase):
            prompt = prompt[len(phrase):].strip()
            break

    return re.sub(r"\s+", " ", prompt)

# ✅ Matches "hi", "hello", "hey" at the beginning (not necessarily pure greeting)
def is_greeting(prompt: str) -> bool:
    return prompt.lower().strip().startswith(("hi", "hello", "hey"))

# ✅ Matches if prompt is ONLY a greeting (used to avoid LLM call)
def is_pure_greeting(prompt: str) -> bool:
    return prompt.lower().strip() in ["hi", "hello", "hey", "hi!", "hello!", "hey!"]
