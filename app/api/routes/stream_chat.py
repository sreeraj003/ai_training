from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.chat import ChatRequest
from app.services.streaming_service import stream_ai_response

router = APIRouter()


@router.post("/chat/stream")
async def stream_chat(request: ChatRequest):

    messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant."
        },
        {
            "role": "user",
            "content": request.message
        }
    ]

    return StreamingResponse(
        stream_ai_response(messages),
        media_type="text/plain"
    )