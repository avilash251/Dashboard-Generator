import os
import google.generativeai as genai
from utils.rag_context import retrieve_context

os.environ["GEMINI_API_KEY"] = "AIzaSyDoxaPFy-Bk4hPQUKGYXrDdlAcNTB0kbus"

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def ask_gemini(user_prompt: str) -> str:
    try:
        full_prompt = f"""
            You are a Prometheus expert. Given the user prompt, return a PromQL query and title in JSON format.

            User Request:
            {user_prompt}

            Respond like:
            {{
            "category": "infrastructure",
            "promql": "server_cpu_usage_percent",
            "chart_type": "line",
            "title": "CPU Usage (%)",
            "thresholds": [80, 90]
            }}
            """
        model = genai.GenerativeModel("gemini-1.5-flash")  # Or 2.5 if you're using that
        response = model.generate_content(full_prompt)
        return response.text.strip()
    except Exception as e:
        return f"Gemini error: {str(e)}"

