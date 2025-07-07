from fastapi import APIRouter, Query
from utils.prometheus_query import query_range

router = APIRouter()

@router.get("/timeseries")
def get_timeseries(
    promql: str = Query(...),
    duration: str = "2h",
    step: str = "60s",
    prometheus_url: str = "http://localhost:9090"
):
    try:
        return query_range(promql, duration, step, prometheus_url)
    except Exception as e:
        return {"error": str(e)}
