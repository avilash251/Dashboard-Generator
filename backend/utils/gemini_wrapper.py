import os
import google.generativeai as genai
from backend.utils.rag_context import retrieve_context
from backend.utils.context_classifier import infer_context_role, infer_context_scope

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def ask_gemini(user_prompt: str) -> str:
    try:
        context = retrieve_context(user_prompt)
        context_role = infer_context_role(user_prompt)
        context_scope = infer_context_scope(user_prompt)

        full_prompt = f"""
You are acting as a {context_role}.

User Request:
{user_prompt}

Scope: {context_scope}

Helpful Context:
{context}

Respond in JSON format with:
- category
- promql
- chart_type
- title
- thresholds
        """
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(full_prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"
