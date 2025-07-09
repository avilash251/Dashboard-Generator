from fastapi import FastAPI
from routes.chat import chat_router
from routes.history import history_router
from routes.suggestion import suggestion_router
from routes.timeseries import router as timeseries_router
from ws.websocket_server import router as ws_router
from dbscripts.audit_db import init_db

app = FastAPI()
init_db()

app.include_router(chat_router, prefix="/api")
app.include_router(history_router, prefix="/api")
app.include_router(suggestion_router, prefix="/api")
app.include_router(timeseries_router, prefix="/api")
app.include_router(ws_router)
