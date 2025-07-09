from fastapi import WebSocket, APIRouter
import json

ws_router = APIRouter()

@ws_router.websocket("/ws/metrics")
async def metrics_stream(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Simulate or fetch real-time metric
            metric = {
                "title": "CPU Usage",
                "type": "cpu",
                "value": 77,
                "timestamp": time.time(),
            }
            await websocket.send_text(json.dumps(metric))
            await asyncio.sleep(5)
    except:
        await websocket.close()
