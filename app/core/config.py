import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    NVIDIA_API_KEY: str = os.getenv("NVIDIA_API_KEY", "")
    NVIDIA_BASE_URL: str = "https://integrate.api.nvidia.com/v1"
    NVIDIA_MODEL: str = "nvidia/nemotron-3.5-super-vl-120b-a12b"

settings = Settings()

if not settings.NVIDIA_API_KEY:
    raise ValueError("NVIDIA_API_KEY is not configured")

if not settings.NVIDIA_BASE_URL:
    raise ValueError("NVIDIA_BASE_URL is not configured")

if not settings.NVIDIA_MODEL:
    raise ValueError("NVIDIA_MODEL is not configured")