from fastapi import FastAPI
from app.api.routes import chat, health
from app.services.chat_session_manager import ChatSessionManager


app = FastAPI(
    title="AI Engineering Backend",
    description="Building production-oriented AI applications",
    version="1.0.0"
)


app.include_router(chat.router)
app.include_router(health.router)


@app.get("/")
def root():
    return {
        "message": "AI Engineering Backend is running!"
    }