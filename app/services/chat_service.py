from app.core.config import settings
from app.schemas.chat import ChatRequest
from app.services.ai_client import async_client
from app.services.chat_session_manager import ChatSessionManager 
sessionManager = ChatSessionManager()
async def process_message(request: ChatRequest):
    session = None
    if(request.session_id not in sessionManager.session):
        sessionManager.create_session(request.session_id) 
    session = sessionManager.get_session(request.session_id)
    session.add_user_message(request.message)
    try:
        messages=session.get_messages()
        completion = await async_client.chat.completions.create(
            model=settings.NVIDIA_MODEL,
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )
        ai_response = completion.choices[0].message.content
        session.add_assistant_message(ai_response)
        return {
            "received_question": request.message,
            "ai_response":ai_response or ""
        }
    except Exception:
        session.messages.pop()
        raise