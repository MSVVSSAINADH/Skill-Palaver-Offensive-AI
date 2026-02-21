import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Cybersecurity Training Platform"
    environment: str = os.getenv("ENVIRONMENT", "development")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    secret_key: str = os.getenv("SECRET_KEY", "default-secret-key")
    debug_mode: bool = os.getenv("DEBUG_MODE", "True").lower() in ("true", "1", "t")

    class Config:
        env_file = ".env"

settings = Settings()
