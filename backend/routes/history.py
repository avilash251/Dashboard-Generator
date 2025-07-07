from fastapi import APIRouter
from dbscripts.audit_db import save_log, get_recent_logs, get_anomaly_trend

router = APIRouter()

@router.get("/history/logs")
def get_logs():
    try:
        return {"logs": get_recent_logs()}
    except Exception as e:
        return {"error": str(e)}

@router.get("/history/trend")
def get_trend():
    try:
        return {"trend": get_anomaly_trend()}
    except Exception as e:
        return {"error": str(e)}

async def save_audit_log(prompt: str, source="user"):
    try:
        save_log(prompt, source)
    except Exception as e:
        print("Audit log error:", e)
