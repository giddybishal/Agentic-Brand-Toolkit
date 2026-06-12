import os

class Settings:
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "dummy_key")
    crawler_timeout: int = int(os.getenv("CRAWLER_TIMEOUT", "30"))

settings = Settings()
