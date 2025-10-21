
from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Optional

class Settings(BaseSettings):
    # Database fields - optional since DATABASE_URL might be used instead
    database_hostname: Optional[str] = None
    database_port: Optional[str] = None
    database_password: Optional[str] = None
    database_name: Optional[str] = None
    database_username: Optional[str] = None
    
    # Required fields for JWT
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    
    class Config:
        # Get project root directory
        env_file = Path(__file__).parent.parent / ".env"
        env_file_encoding = "utf-8"
        extra = 'ignore' 

settings = Settings()