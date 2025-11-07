from pydantic_settings import BaseSettings
from pydantic import AnyUrl


class Settings(BaseSettings):
    APP_NAME: str = "WebSocket Chat API"
    HOST: str = "0.0.0.0"
    PORT: int = 8004
    LOG_LEVEL: str = "INFO"
    CORS_ORIGIN: list[str] = ["http://localhost:8004", "http://127.0.0.1:8004"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()