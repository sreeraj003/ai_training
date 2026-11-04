from app.core.config import settings

def process_message(message: str):
    return {
        "received_question": message,
        "message": "Your question was received successfully."
    }
    
print(f"NVIDIA API Key: {settings.NVIDIA_API_KEY}")