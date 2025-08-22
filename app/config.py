import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./app.db"
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "logs/app.log"
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # API
    api_prefix: str = "/api"
    title: str = "User Account and Tasks API"
    version: str = "1.0.0"
    description: str = "API for managing user accounts and tasks"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
