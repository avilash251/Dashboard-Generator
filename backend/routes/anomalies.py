from fastapi import APIRouter, Query
from utils.prometheus_query import query_range
from datetime import datetime
from routes.history import save_audit_log
import numpy as np

router = APIRouter()

def detect_anomalies(values, threshold=2.5):
    try:
        vals = np.array([float(v[1]) for v in values])
        mean, std = np.mean(vals), np.std(vals)
        return [
            {"timestamp": v[0], "value": float(v[1])}
            for v in values if abs((float(v[1]) - mean) / std) > threshold
        ]
    except:
        return []

@router.get("/anomalies")
async def get_anomalies(promql: str):
    try:
        result = query_range(promql, "2h", "60s", "http://localhost:9090")
        data = result.get("data", {}).get("values", [])
        anomalies = detect_anomalies(data)

        if anomalies:
            await save_audit_log(f"{len(anomalies)} anomalies in {promql}", "system")

        return {"anomalies": anomalies, "count": len(anomalies)}
    except Exception as e:
        return {"error": str(e)}
