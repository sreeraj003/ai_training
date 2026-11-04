from pydantic import BaseModel, Field, field_validator


class ChatRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=2000,
        description="Question submitted by the user"
    )

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str):
        value = value.strip()
        print(f"Validating message: '{value}'")  # Debugging statement
        if not value:
            raise ValueError("Message cannot be empty or whitespace.")

        return value
class ChatResponse(BaseModel):
    received_question: str
    message: str