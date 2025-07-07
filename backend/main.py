from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from routes.chat import chat_router
from routes.timeseries import router as timeseries_router
from routes.history import router as history_router
from routes.anomalies import router as anomaly_router
from routes.suggestion import router as suggestion_router
from dbscripts.audit_db import init_db
import socketio
from dbscripts.init_db import init_db


# --- Socket.IO Setup ---
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")
fastapi_app = FastAPI()

# Add middleware
fastapi_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount all routes
init_db()
fastapi_app.include_router(chat_router, prefix="/api")
fastapi_app.include_router(timeseries_router, prefix="/api")
fastapi_app.include_router(history_router, prefix="/api")
fastapi_app.include_router(anomaly_router, prefix="/api")
fastapi_app.include_router(suggestion_router, prefix="/api")

# Wrap FastAPI with Socket.IO
app = socketio.ASGIApp(sio, other_asgi_app=fastapi_app)


# --- Socket Events ---
@sio.event
async def connect(sid, environ):
    print(f"✅ Client connected: {sid}")
    await sio.emit("live-status", {"status": "🟢 Live"}, to=sid)

@sio.event
async def disconnect(sid):
    print(f"❌ Client disconnected: {sid}")
