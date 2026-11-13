
import asyncio

from app.services.chat_summary_manager import SummaryManager
from app.services.conversation_manager import ConversationManager


class ChatSessionManager:

    def __init__(self):
        self.session = {}
        self.locks = {}

    def create_session(self, session_id: str):
        if session_id in self.session:
            raise ValueError("Session already exists")

        self.session[session_id] = {
            "conversation": ConversationManager(),
            "memory": SummaryManager()
        }

        self.locks[session_id] = asyncio.Lock()

    def get_session(self, session_id: str):
        if session_id not in self.session:
            raise ValueError("Session does not exist")

        return self.session[session_id]

    def get_lock(self, session_id: str):
        if session_id not in self.locks:
            raise ValueError("Session lock does not exist")

        return self.locks[session_id]

    def delete_session(self, session_id: str):
        if session_id not in self.session:
            raise ValueError("Session does not exist")

        del self.session[session_id]
        del self.locks[session_id]

    def get_conversation(self, session_id: str):
        return self.get_session(session_id)["conversation"]

    def get_memory(self, session_id: str):
        return self.get_session(session_id)["memory"]
