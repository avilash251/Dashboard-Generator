from socketio import AsyncServer
sio = AsyncServer(async_mode="asgi", cors_allowed_origins="*")

@sio.event
async def connect(sid, environ):
    print("✅ Client connected:", sid)

async def emit_live_status():
    await sio.emit("live-status", {"status": "🟢 Live"})

async def emit_metric_update(metric_name: str, value: float):
    await sio.emit("metric-update", {"metric": metric_name, "value": value})
