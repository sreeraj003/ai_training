import json
from pydantic import ValidationError
from app.core.config import settings
from app.schemas.memory import MemoryExtractionResponse

class MemoryExtractor:

    def __init__(self, ai_client):
        self.ai_client = ai_client

    async def extract_memories(self, messages: list, current_memory: dict):
        extraction_messages = self.build_extraction_messages(
            messages,
            current_memory
        )

        completion = await self.ai_client.chat.completions.create(
            model=settings.NVIDIA_MODEL,
            messages=extraction_messages,
            temperature=0
        )

        raw_response = completion.choices[0].message.content
        if not raw_response or not raw_response.strip():
            raise ValueError("LLM returned an empty response.")
        try:
            parsed_response = json.loads(raw_response)
            validated_response = MemoryExtractionResponse.model_validate(
            parsed_response
            )
            return validated_response
        except  ValidationError as error:
            print("invalid memory data:",error)
            raise ValueError("Invalid memory data received from AI model.",raw_response)
        
    def build_extraction_messages(self, messages: list, current_memory: dict):
        MEMORY_EXTRACTION_PROMPT = """You are a memory extraction assistant. Your task is to extract useful, long-term information from the conversation.
        Available categories:
            - user_facts
            - preferences
            - decisions
            - ongoing_tasks
            - unresolved_tasks
            - learning_journey

            Rules:
            1. Extract only information explicitly supported by the conversation.
            2. Do not invent or assume facts.
            3. Update existing information when the user provides
            a newer status or correction.
            4. Do not store temporary or irrelevant conversation details.
            5. Return only valid JSON. Do not use Markdown code fences.
            6. If there is no useful new information, return:
            {"updates": []}

            7. The response MUST be a JSON object with an "updates" property.
            The "updates" property must contain an array of memory objects.

            8. Each memory object MUST contain exactly these three fields:
            - category: string
            - key: string
            - value: any JSON-compatible value

            9. Do not return a standalone array. Do not add any additional fields.

            10. Follow this exact structure:
            {
                "updates": [
                    {
                        "category": "learning_journey",
                        "key": "current_language",
                        "value": "Python"
                    }
                ]
            }
            """
        return [
            {
                "role": "system",
                "content":MEMORY_EXTRACTION_PROMPT
            },
            {
                "role": "user",
                "content": json.dumps({
                    "conversation": messages,
                    "current_memory": current_memory
                })
            }
        ]
                
            