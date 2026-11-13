from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.chat import ChatRequest
from app.services.chat_service import process_stream_message

router = APIRouter()


@router.post("/chat/stream")
async def stream_chat(request: ChatRequest):

    return StreamingResponse(
        process_stream_message(request),
        media_type="text/plain"
    )