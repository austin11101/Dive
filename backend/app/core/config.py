from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    # Application settings
    APP_NAME: str = "CV Revamping API"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database - Use SQLite for local development
    DATABASE_URL: str = "sqlite:///./cv_database.db"

    # Redis - Disable for local development
    REDIS_URL: str = "redis://localhost:6379"

    # CORS
    ALLOWED_HOSTS: List[str] = [
        "http://localhost:4200",
        "http://127.0.0.1:4200",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:33869",
        "http://127.0.0.1:33869"
    ]

    # File upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIR: str = "uploads"

    # Email settings (for notifications)
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None

    # External services
    OPENAI_API_KEY: Optional[str] = None

    class Config:
        # Don't load from .env file for local development
        env_file = None
        case_sensitive = True


# Create settings instance
settings = Settings()

# Validate required settings in production
if settings.ENVIRONMENT == "production":
    if settings.SECRET_KEY == "your-secret-key-change-in-production":
        raise ValueError("SECRET_KEY must be set in production")

    if "*" in settings.ALLOWED_HOSTS:
        raise ValueError("ALLOWED_HOSTS must be specific in production")
