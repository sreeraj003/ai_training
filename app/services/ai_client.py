from openai import AsyncOpenAI

from app.core.config import settings


async_client = AsyncOpenAI(
    base_url=settings.NVIDIA_BASE_URL,
    api_key=settings.NVIDIA_API_KEY,
    timeout=60.0,
    max_retries=2
)