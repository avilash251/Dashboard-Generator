from rapidfuzz import fuzz

# Static context map with fuzzy matchable keys
PROMQL_CONTEXT_MAP = {
    "cpu": [
        "CPU usage can be collected using node_exporter: rate(node_cpu_seconds_total[5m]).",
        "Per pod CPU usage: rate(container_cpu_usage_seconds_total[5m]) by (pod)."
    ],
    "memory": [
        "Memory usage via node_exporter: node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes.",
        "Memory usage per container: container_memory_usage_bytes."
    ],
    "disk": [
        "Disk I/O usage: rate(node_disk_io_time_seconds_total[5m]).",
        "Free disk space: node_filesystem_avail_bytes."
    ],
    "network": [
        "Network in/out: rate(container_network_receive_bytes_total[5m]) or transmit.",
        "Rate of dropped packets: rate(node_network_dropped_total[5m])."
    ],
    "latency": [
        "Histogram quantile for latency: histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le)).",
        "P95 latency per pod: histogram_quantile(0.95, rate(pod_latency_bucket[5m])) by (pod)."
    ],
    "error": [
        "HTTP 5xx error rate: rate(http_requests_total{status=~\"5..\"}[5m]).",
        "Application error rate: rate(app_errors_total[5m])."
    ],
    "uptime": [
        "Node uptime: node_time_seconds - node_boot_time_seconds.",
        "Container uptime: time() - container_start_time_seconds."
    ]
}

# Fuzzy matching fallback
def retrieve_context(prompt: str) -> str:
    prompt_lower = prompt.lower()
    best_score = 0
    best_key = None

    for key in PROMQL_CONTEXT_MAP.keys():
        score = fuzz.partial_ratio(prompt_lower, key)
        if score > best_score:
            best_score = score
            best_key = key

    if best_key and best_score >= 65:
        return "\n".join(PROMQL_CONTEXT_MAP[best_key])
    else:
        return "No relevant context found. Please refine your prompt."
