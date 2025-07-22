LAYOUT_PROMPT = """
JSON output only.

- statscards: [{title, value, unit}]
- charts: [{title, promql, type}]
- performance_alerts: {high_cpu_hosts: [], underutilized_hosts: []}

Summary:
\"\"\"{summary}\"\"\"
"""
