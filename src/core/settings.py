from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Crypto-trading"
    DEBUG: bool

    POSTGRES_DSN: PostgresDsn

    REDIS_PASSWORD: str
    REDIS_SENTINEL_HOSTS: str
    REDIS_SENTINEL_MASTER_NAME: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_SECONDS: int = 86400
    JWT_REFRESH_TOKEN_EXPIRE_SECONDS: int = 604800

    WALLET_ENCRYPTION_PASSWORD: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
