from cachetools.func import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Ticketing System Gateway"
    APP_VERSION: str = "1.0.0"

    DATABASE_URL: str
    POOL_SIZE: int = 10
    MAX_OVERFLOW: int = 15
    EXPIRE_ON_COMMIT : bool = False
    SQL_ECHO: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()