from functools import lru_cache

from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    ENV_STATE: str | None = "dev"


class Config(BaseConfig):
    DB_URL: str | None = None
    ECHO: bool = False
    DB_FORCE_ROLLBACK: bool = False
    SECRET_KEY: str = "12345"
    ALGORITHM: str = "HS512"
    TOKEN_EXPIRE_SECONDS: int = 5 * 60
    VERIFY_EXPIRE_SECONDS: int = 60 * 60
    TOKEN_PATH: str = "api/v1/auth/token"
    ADMIN_EMAIL: EmailStr = "admin@admin.com"
    ADMIN_PASSWORD: str = "123"
    LOG_LEVEL: str = "INFO"


class TestConfig(Config):
    DB_URL: str | None = "sqlite:///test.db"
    DB_FORCE_ROLLBACK: bool = True


class DevConfig(Config):
    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="DEV_", extra="ignore"
    )
    TOKEN_EXPIRE_SECONDS: int = 30 * 60 * 12
    LOG_LEVEL: str = "DEBUG"


class ProdConfig(Config):
    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="PROD_", extra="ignore"
    )


@lru_cache()
def get_config(env: str = "dev") -> TestConfig | DevConfig | ProdConfig:
    return dict(test=TestConfig, dev=DevConfig, prod=ProdConfig)[env](ENV_STATE=env)


config = get_config(env=BaseConfig().ENV_STATE)
