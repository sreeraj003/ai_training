from pydantic import BaseModel, ConfigDict
from typing import Any, Literal

MemoryCategory = Literal[
    "user_facts",
    "preferences",
    "decisions",
    "ongoing_tasks",
    "unresolved_tasks",
    "learning_journey"
]

class MemoryUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")
    category: MemoryCategory
    key: str
    value: Any

class MemoryExtractionResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    updates: list[MemoryUpdate]