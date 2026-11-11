from app.services.chat_summary_manager import SummaryManager
from app.services.memory_update_processor import MemoryUpdateProcessor
from app.schemas.memory import MemoryExtractionResponse

# Create memory manager
memory = SummaryManager()

# Create update processor
processor = MemoryUpdateProcessor(memory)

# TEST A: Insert new memories
response_a = MemoryExtractionResponse.model_validate({
    "updates": [
        {
            "category": "learning_journey",
            "key": "current_language",
            "value": "Python"
        },
        {
            "category": "learning_journey",
            "key": "target_role",
            "value": "AI engineer"
        }
    ]
})

processor.apply_updates(response_a)


# TEST B: Update existing memory
response_b = MemoryExtractionResponse.model_validate({
    "updates": [
        {
            "category": "learning_journey",
            "key": "current_language",
            "value": "FastAPI"
        }
    ]
})

processor.apply_updates(response_b)

print(MemoryExtractionResponse.model_json_schema())
