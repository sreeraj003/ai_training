from app.services.ai_client import async_client
from app.core.config import settings


async def stream_ai_response(messages: list):

    print("1. Starting NVIDIA request")

    stream = await async_client.chat.completions.create(
        model=settings.NVIDIA_MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=1000,
        stream=True
    )

    print("2. NVIDIA stream established")

    async for chunk in stream:

        print("CHUNK:", chunk.model_dump())

        if not chunk.choices:
            continue

        content = chunk.choices[0].delta.content

        if content:
            print("CONTENT:", repr(content))
            yield content

    print("5. Stream completed")