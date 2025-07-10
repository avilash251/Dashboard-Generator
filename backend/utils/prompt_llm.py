template_prompt = f"""
You are a PromQL expert. Convert the following natural language query into an accurate PromQL query.

Return only the PromQL expression.

Examples:
"Show CPU usage across all nodes" → avg(rate(node_cpu_seconds_total{{mode!="idle"}}[5m])) by (instance)
"Memory usage per pod" → sum(container_memory_usage_bytes{{container!=""}}) by (pod)

Now convert this:
"{user_query}"
"""
