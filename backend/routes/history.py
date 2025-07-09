from fastapi import APIRouter
from dbscripts.audit_db import save_log, get_recent_logs, get_anomaly_trend

history_router = APIRouter()

@history_router.post("/history/log")
async def log_prompt(prompt: str, source: str = "user"):
    save_log(prompt, source)
    return {"status": "ok"}

@history_router.get("/history/recent")
async def get_history():
    logs = get_recent_logs()
    return [{"prompt": log.prompt, "source": log.source, "timestamp": str(log.timestamp)} for log in logs]

@history_router.get("/history/anomalies")
async def get_anomalies():
    logs = get_anomaly_trend()
    return [{"metric": log.metric, "severity": log.severity, "timestamp": str(log.timestamp)} for log in logs]
