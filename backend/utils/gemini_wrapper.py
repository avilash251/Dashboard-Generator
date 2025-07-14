import json
from utils.context_classifier import infer_context_role, infer_context_scope
from utils.retrieve_context import retrieve_context
from utils.gemini_wrapper import model
from dbscripts.audit_db import save_log

def build_gemini_prompt(user_prompt: str, context: str, role: str, scope: str) -> str:
    return f"""
You are a Prometheus dashboard assistant. Your job is to convert user requests into dashboard layouts using PromQL.

User Prompt:
\"\"\"{user_prompt}\"\"\"

Context Role: {role}
Context Scope: {scope}

PromQL Knowledge:
\"\"\"{context}\"\"\"

Return a JSON with keys: intent, context_role, context_scope, layout, suggestions.

Layout format:
[
  {{
    "title": "string",
    "promql": "string",
    "chart_type": "line" | "bar" | "area",
    "thresholds": {{
      "warning": number,
      "critical": number
    }}
  }}
]

Output only valid JSON. No extra text.
"""

def ask_gemini(user_prompt: str) -> dict:
    try:
        # Step 1: Retrieve additional context
        context = retrieve_context(user_prompt)
        role = infer_context_role(user_prompt)
        scope = infer_context_scope(user_prompt)

        prompt = build_gemini_prompt(user_prompt, context, role, scope)

        # Step 2: Call Gemini or OpenAI endpoint
        response = model.generate_content(prompt)
        output = json.loads(response.text.strip())

        # Step 3: Log the entire interaction to DB
        save_log({
            "user_prompt": user_prompt,
            "response": output,
            "context_role": output.get("context_role", role),
            "context_scope": output.get("context_scope", scope),
            "intent": output.get("intent", "unknown"),
            "source": "gemini"
        })

        return output

    except Exception as e:
        print(f"[Gemini Error] {e}")
        save_log({
            "user_prompt": user_prompt,
            "response": str(e),
            "context_role": "error",
            "context_scope": "error",
            "intent": "error",
            "source": "gemini"
        })
        return {
            "intent": "unknown",
            "context_role": "generic",
            "context_scope": "generic",
            "layout": [],
            "suggestions": ["Please rephrase or clarify your request."]
        }
