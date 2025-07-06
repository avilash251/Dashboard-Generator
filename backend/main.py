from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.chat import router as chat_router
from routes.timeseries import router as timeseries_router
from routes.suggestions import router as suggestions_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/api")
app.include_router(timeseries_router, prefix="/api")
app.include_router(suggestions_router, prefix="/api")

@app.get("/")
def root():
    return {"status": "Gemini Dashboard Running"}
