from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database settings
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "tgstat_db"
    
    # TGStat API settings
    TGSTAT_API_TOKEN: Optional[str] = None
    TGSTAT_API_BASE_URL: str = "https://api.tgstat.ru"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

