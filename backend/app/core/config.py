from functools import lru_cache

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Buildlog API"
    app_env: str = "development"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "postgresql+psycopg://buildlog:buildlog@localhost:5432/buildlog"
    jwt_secret_key: str = "dev-only-change-this-secret-before-deployment"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @model_validator(mode="after")
    def validate_security_settings(self):
        if self.app_env.lower() == "production":
            if self.jwt_secret_key == "dev-only-change-this-secret-before-deployment":
                raise ValueError("Set a unique JWT_SECRET_KEY in production")
            if len(self.jwt_secret_key) < 32:
                raise ValueError("JWT_SECRET_KEY must be at least 32 characters")
        if self.access_token_expire_minutes < 1:
            raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES must be positive")
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
