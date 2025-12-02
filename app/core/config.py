"""
Application configuration settings.
"""
from pydantic_settings import BaseSettings
from typing import List, Optional


class Settings(BaseSettings):
    """Application settings."""
    
    # App
    APP_NAME: str = "PRATT - IDCC Requirements Assistant"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite:///./pratt.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: List[str] = ["*"]
    
    # File uploads
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # OCR
    TESSERACT_CMD: Optional[str] = None  # Will use system default if None
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()


