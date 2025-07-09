from rapidfuzz import fuzz

# 🔧 Predefined static context mapping
PROMQL_CONTEXT_MAP = {
    "cpu": "CPU usage is typically collected using: rate(node_cpu_seconds_total[5m]).",
    "memory": "Memory usage can be monitored with: node_memory_Active_bytes or node_memory_MemAvailable_bytes.",
    "disk": "Disk metrics use: node_filesystem_free_bytes, node_disk_read_bytes_total, node_disk_written_bytes_total.",
    "uptime": "System uptime can be fetched using: node_boot_time_seconds.",
    "http_errors": "HTTP error rates (like 5xx) use: rate(http_requests_total{status=~\"5..\"}[5m]).",
    "network": "Network stats: rate(node_network_receive_bytes_total[5m]), rate(node_network_transmit_bytes_total[5m]).",
    "pod": "Pod metrics example: sum(container_memory_usage_bytes) by (pod).",
    "node_latency": "Node latency is often tracked using histogram_quantile over request_duration_seconds metrics.",
    "disk_io": "Disk I/O trend: rate(node_disk_io_time_seconds_total[5m]).",
    "namespace": "Namespace-specific memory: sum(container_memory_usage_bytes) by (namespace)."
}

def retrieve_context(user_prompt: str) -> str:
    """
    Use fuzzy match to find the most relevant context string based on the prompt.
    """
    try:
        best_key = None
        best_score = 0

        for key, description in PROMQL_CONTEXT_MAP.items():
            score = fuzz.partial_ratio(user_prompt.lower(), key.lower())
            if score > best_score:
                best_score = score
                best_key = key

        if best_score >= 70 and best_key:
            return PROMQL_CONTEXT_MAP[best_key]
        return "No specific context found for the given prompt."
    except Exception as e:
        return f"Context resolution error: {str(e)}"
