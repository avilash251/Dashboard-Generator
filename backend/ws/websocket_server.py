# websocket_manager.py
from fastapi import WebSocket

class WebSocketManager:
    def __init__(self):
        self.connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def broadcast(self, message: str):
        for ws in self.connections:
            try:
                await ws.send_text(message)
            except:
                pass  # silently fail or clean up dead sockets

ws_manager = WebSocketManager()
