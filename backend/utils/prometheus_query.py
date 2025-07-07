import requests
from datetime import datetime, timedelta

def query_range(promql, duration="1h", step="60s", prometheus_url="http://localhost:9090"):
    try:
        now = datetime.utcnow()
        start = now - timedelta(hours=int(duration.replace("h", "")))
        params = {
            "query": promql,
            "start": start.timestamp(),
            "end": now.timestamp(),
            "step": step
        }
        r = requests.get(f"{prometheus_url}/api/v1/query_range", params=params)
        return r.json().get("data", {}).get("result", [{}])[0]
    except Exception as e:
        return {"error": str(e)}
