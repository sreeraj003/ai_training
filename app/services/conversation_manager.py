class ConversationManager:
    system_message={
        "role": "system",
        "content": "You are a helpful technical assistant. Answer clearly and practically."
    }
    def __init__(self):
        self.message = [self.system_message.copy()]
        
    def add_user_message(self,message:str):
        self.message.append({"role":"user","content":message})
    
    def add_assistant_message(self, message: str):
        self.message.append({
            "role": "assistant",
            "content": message
        })

    def get_messages(self):
        return [message.copy() for message in self.message]

    def clear_history(self):
        self.message = [self.system_message.copy()]