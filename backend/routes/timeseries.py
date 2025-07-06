from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import requests

router = APIRouter()  # ✅ This is what must exist!

PROMETHEUS_URL = os.getenv("PROMETHEUS_URL", "http://localhost:9090")

class TimeSeriesRequest(BaseModel):
    promql: str
    prometheus_url: str = "http://localhost:9090"

@router.post("/timeseries/query")
def query_timeseries(req: TimeSeriesRequest):
    try:
        response = requests.get(f"{req.prometheus_url}/api/v1/query", params={"query": req.promql})
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prometheus query failed: {str(e)}")
