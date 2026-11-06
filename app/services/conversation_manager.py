class ConversationManager:

    SYSTEM_MESSAGE = {
        "role": "system",
        "content": "You are a helpful technical assistant. Answer clearly and practically."
    }

    def __init__(self):
        self.messages = [self.SYSTEM_MESSAGE.copy()]

    def add_user_message(self, message: str):
        self.messages.append({
            "role": "user",
            "content": message
        })

    def add_assistant_message(self, message: str):
        self.messages.append({
            "role": "assistant",
            "content": message
        })

    def get_messages(self):
        return [message.copy() for message in self.messages]

    def clear_history(self):
        self.messages = [self.SYSTEM_MESSAGE.copy()]

    def trim_history(self, max_tokens: int, token_manager):

        while token_manager.count_messages_tokens(self.messages) > max_tokens:

            if len(self.messages) <= 1:
                break

            del self.messages[1:3]