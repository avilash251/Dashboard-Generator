from fastapi import APIRouter

router = APIRouter()

@router.get("/suggestion")
def get_suggestions():
    try:
        return {
            "suggestions": [
                "Show CPU usage for server1",
                "Disk I/O trend over last 6 hours",
                "HTTP 5xx error rate",
                "Memory usage for namespace kube-system",
                "Node latency P95 for cluster1"
            ]
        }
    except Exception as e:
        return {"error": str(e)}
