"""Configuration settings for DataScientist Arena"""

from pydantic_settings import BaseSettings
from typing import List
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]
    
    # Database
    DATABASE_URL: str = "sqlite:///./data_science_arena.db"
    
    # File uploads
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024  # 50MB
    
    # LLM Configuration
    LLM_API_URL: str = "http://localhost:11434"
    LLM_MODEL: str = "mistral"
    LLM_TEMPERATURE: float = 0.3
    LLM_MAX_TOKENS: int = 2000
    LLM_TIMEOUT: int = 60
    
    # Execution
    EXECUTION_TIMEOUT: int = 300  # 5 minutes
    MAX_CONCURRENT_RUNS: int = 2
    
    # Verification
    VERIFICATION_ENABLED: bool = True
    ERROR_INJECTION_ENABLED: bool = True
    
    # Research
    BENCHMARK_DIR: str = "./benchmarks"
    RESULTS_DIR: str = "./results"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings():
    """Get cached settings"""
    return Settings()

settings = get_settings()
