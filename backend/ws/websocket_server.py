from fastapi import WebSocket, APIRouter, WebSocketDisconnect
import asyncio
import time
import random

router = APIRouter()
clients = set()

@router.websocket("/ws/metrics")
async def ws_metrics(websocket: WebSocket):
    await websocket.accept()
    clients.add(websocket)
    try:
        while True:
            data = {"metric": "CPU Usage", "value": random.randint(20, 80), "timestamp": time.time()}
            for client in clients:
                await client.send_json(data)
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        clients.remove(websocket)
