
from typing import List
from collections import Counter
from rapidfuzz import fuzz
import json

# Static grouped suggestions (base)
SUGGESTION_GROUPS = {
    "CPU": [
        "Show CPU usage for <node>",
        "Top pods by CPU usage",
        "Compare CPU utilization for nodes"
    ],
    "Memory": [
        "Memory usage for <namespace>",
        "Alert if memory exceeds threshold",
        "Container memory usage over time"
    ],
    "Disk": [
        "Disk I/O metrics for <node>",
        "Disk space remaining across volumes",
        "Disk usage anomalies in private cloud"
    ],
    "Network": [
        "Network bandwidth across interfaces",
        "Packet drop rate on <node>",
        "Ingress traffic for <service>"
    ],
    "Errors": [
        "HTTP 5xx error rate for services",
        "TLS handshake failures on ingress",
        "Database connection errors"
    ],
    "Cloud": [
        "Resource usage in public cloud",
        "Cluster usage in private cloud"
    ],
}

# Flattened list of all suggestions
FLATTENED_SUGGESTIONS = [s for group in SUGGESTION_GROUPS.values() for s in group]

# Simulate recent prompt history (replace with DB in real use)
RECENT_PROMPTS = Counter()

def filter_suggestions(query: str = "") -> List[str]:
    if not query or len(query) < 3:
        return FLATTENED_SUGGESTIONS[:10]  # Default top suggestions

    query = query.lower()
    scored = [
        (s, fuzz.token_set_ratio(query, s.lower()))
        for s in FLATTENED_SUGGESTIONS
    ]
    return [s for s, score in sorted(scored, key=lambda x: x[1], reverse=True) if score > 60][:10]

def record_prompt(prompt: str):
    RECENT_PROMPTS[prompt.strip()] += 1

def get_top_recent_prompts(limit: int = 5) -> List[str]:
    return [item[0] for item in RECENT_PROMPTS.most_common(limit)]

def get_grouped_suggestions() -> dict:
    return SUGGESTION_GROUPS
