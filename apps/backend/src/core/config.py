from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FashNet"
    
    # MongoDB
    MONGO_URL: str
    MONGO_DB_NAME: str
    
    # Security
    JWT_SECRET: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Services
    MODEL_SERVICE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
