from pydantic import PostgresDsn
from pydantic_settings import SettingsConfigDict, BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: PostgresDsn
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
