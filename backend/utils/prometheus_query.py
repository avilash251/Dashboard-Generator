import requests

PROMETHEUS_URL = "http://localhost:9090"  # Update to actual URL if needed

def query_prometheus(promql: str, time: str = None):
    try:
        params = {"query": promql}
        if time:
            params["time"] = time
        response = requests.get(f"{PROMETHEUS_URL}/api/v1/query", params=params, timeout=5)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def query_range(promql: str, start: str, end: str, step: str = "30s"):
    try:
        params = {
            "query": promql,
            "start": start,
            "end": end,
            "step": step
        }
        response = requests.get(f"{PROMETHEUS_URL}/api/v1/query_range", params=params, timeout=5)
        return response.json()
    except Exception as e:
        return {"error": str(e)}
