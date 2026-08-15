from dotenv import load_dotenv
from pydantic import PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "Crypto-trading"
    DEBUG: bool

    POSTGRES_DSN: PostgresDsn
    REDIS_DSN: RedisDsn

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_SECONDS: int = 86400
    JWT_REFRESH_TOKEN_EXPIRE_SECONDS: int = 604800

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
