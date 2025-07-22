from starlette.websockets import WebSocket, WebSocketState
from typing import Dict

# Structure: { user_id: { "socket": WebSocket, "ip": str, "connected_at": str } }
socket_registry: Dict[str, Dict] = {}

def register_socket(user_id: str, websocket: WebSocket, ip: str):
    socket_registry[user_id] = {
        "socket": websocket,
        "ip": ip,
        "connected_at": "now"  # You can set datetime.utcnow().isoformat() if needed
    }

def remove_socket(user_id: str):
    if user_id in socket_registry:
        del socket_registry[user_id]

def get_socket(user_id: str) -> WebSocket | None:
    entry = socket_registry.get(user_id)
    if entry:
        return entry["socket"]
    return None

def get_registry_snapshot() -> dict:
    return {uid: {k: v for k, v in meta.items() if k != "socket"} for uid, meta in socket_registry.items()}
