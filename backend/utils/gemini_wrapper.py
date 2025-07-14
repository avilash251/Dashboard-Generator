import json
from utils.context_classifier import infer_context_role, infer_context_scope
from utils.retrieve_context import retrieve_context
from utils.gemini_wrapper import model  # replace with OpenAI/Gemini wrapper as used

def build_gemini_prompt(user_prompt: str, context: str, role: str, scope: str) -> str:
    return f"""
You are a highly skilled Prometheus monitoring assistant. Your task is to interpret a user’s natural language query and translate it into a structured dashboard definition using PromQL.

Given the user prompt below:

🔸 User Prompt:
\"\"\"{user_prompt}\"\"\"

You must determine:

1️⃣ intent — The main purpose of the request. Be specific. Examples: "cpu_usage_by_node", "memory_by_namespace", "disk_io_per_pod", etc.

2️⃣ context_role — The monitoring scope: ["infrastructure", "application", "cluster", "cloud", "network", etc.]

3️⃣ context_scope — The level of granularity (e.g., "per pod", "by namespace", "node-level", "per server", or "generic" if not inferable)

4️⃣ layout — A JSON array of recommended PromQL visualizations. Each item must have:

```json
[
  {{
    "title": "string",
    "promql": "string",
    "chart_type": "line" | "bar" | "area",
    "thresholds": {{
      "warning": number (optional),
      "critical": number (optional)
    }}
  }}
]
