
import logging

from app.core.config import settings
from app.schemas.chat import ChatRequest
from app.services.ai_client import async_client
from app.services.chat_session_manager import ChatSessionManager
from app.services.memory_update_processor import MemoryUpdateProcessor
from app.services.token_manager import TokenManager
from app.services.context_manager import ContextManager
from app.services.MemoryExtractor import MemoryExtractor

logger = logging.getLogger(__name__)

session_manager = ChatSessionManager()
token_manager = TokenManager()

memory_extractor = MemoryExtractor(async_client)

context_manager = ContextManager(
    token_manager=token_manager,
    context_limit=32000,
    output_reserve=4500,
    safety_margin=5000
)


async def process_message(request: ChatRequest):

    if request.session_id not in session_manager.session:
        session_manager.create_session(request.session_id)

    conversation = session_manager.get_conversation(
        request.session_id
    )

    memory = session_manager.get_memory(
        request.session_id
    )

    conversation.add_user_message(request.message)

    try:
        # Stage 1: Generate assistant response

        messages = conversation.add_memory_to_system_message(
            memory.get_summary()
        )

        trimmed_messages = context_manager.trim_msg(messages)

        completion = await async_client.chat.completions.create(
            model=settings.NVIDIA_MODEL,
            messages=trimmed_messages,
            max_tokens=1000,
            temperature=0.7
        )

        ai_response = completion.choices[0].message.content or ""

        conversation.add_assistant_message(ai_response)

    except Exception:
        # Roll back only the failed chat operation.
        if conversation.messages and conversation.messages[-1]["role"] == "user":
            conversation.remove_last_user_message()

        raise

    # Stage 2: Memory extraction
    # Memory failure must not invalidate the successful chat response.

    try:
        extraction_response = await memory_extractor.extract_memories(
            conversation.get_messages(),
            memory.get_summary()
        )

        processor = MemoryUpdateProcessor(memory)

        processor.apply_updates(extraction_response)

    except Exception:
        logger.exception("Memory extraction or update failed")

    return {
        "received_question": request.message,
        "ai_response": ai_response
    }
