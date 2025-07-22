LAYOUT_PROMPT = """
You are an infrastructure layout generation agent.

Your task is to convert the following plain-text infrastructure summary into a structured layout JSON object for dashboard rendering.

The layout must include:
1. "statscards": key system stats like CPU cores, memory, disk, OS, environment, total servers
2. "charts": PromQL-based chart placeholders (title, promql, type)
3. "performance_alerts": include hostnames with high CPU and low utilization

Ensure the output is a valid JSON. Do not include markdown or explanations.

Here is the summary:
\"\"\"{summary}\"\"\"
"""
