import tiktoken


class TokenManager:

    def __init__(self):
        self.encoding = tiktoken.get_encoding("cl100k_base")

    def count_tokens(self, text: str) -> int:
        return len(self.encoding.encode(text))

    def count_messages_tokens(self, messages: list) -> int:
        total = 0

        for message in messages:
            total += self.count_tokens(message["content"])
            total += self.count_tokens(message["role"])

        return total
    
