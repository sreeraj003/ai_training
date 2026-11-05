from app.services.conversation_manager import ConversationManager

class ChatSessionManager:
    def __init__(self):
        self.session={}
    
    def create_session(self,session_id:str):
        if(session_id in self.session):
            raise ValueError(f"Session with ID {session_id} already exists.")
        self.session[session_id] = ConversationManager()
        
    def get_session(self,session_id:str):
        if(session_id not in self.session):
            raise ValueError(f"Session with ID {session_id} does not exist.")
        return self.session[session_id]
    
    def delete_session(self,session_id:str):
        if(session_id not in self.session):
            raise ValueError(f"Session with ID {session_id} does not exist.")
        del self.session[session_id]
        
