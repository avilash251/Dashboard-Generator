# routes/timeseries.py
from fastapi import APIRouter, Request
from utils.prometheus_query import query_prometheus, query_range

router = APIRouter()

@router.post("/timeseries")
async def get_timeseries(request: Request):
    try:
        body = await request.json()
        promql = body.get("promql")
        mode = body.get("mode", "instant")  # "instant" or "range"
        step = body.get("step", "30s")
        start = body.get("start")
        end = body.get("end")

        if not promql:
            return {"error": "promql is required"}

        if mode == "range":
            if not start or not end:
                return {"error": "start and end times are required for range mode"}
            result = query_range(promql, start=start, end=end, step=step)
        else:
            result = query_prometheus(promql)

        return result
    except Exception as e:
        return {"error": str(e)}
