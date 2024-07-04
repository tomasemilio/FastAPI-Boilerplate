from functools import cache

from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    ENV_STATE: str = "dev"
    DROP_ENVS: list[str] = ["test"]


class Config(BaseConfig):
    DB_URL: str = "sqlite+aiosqlite:///test.db"
    SECRET_KEY: str = "123"
    ALGORITHM: str = "HS512"
    TOKEN_EXPIRE_SECONDS: int = 3600
    RESET_EXPIRE_SECONDS: int = 300
    TOKEN_PATH: str = "api/v1/auth/token"
    ADMIN_EMAIL: EmailStr = "admin@sample.com"
    ADMIN_PASSWORD: str = "123"
    ADMIN_EMAIL_TOKEN: str = "123"
    LOG_LEVEL: str = "DEBUG"


class TestConfig(Config):
    DB_URL: str = "sqlite+aiosqlite:///test.db"
    LOG_LEVEL: str = "DEBUG"


class DevConfig(Config):
    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="DEV_", extra="ignore"
    )
    DB_URL: str = "sqlite+aiosqlite:///dev.db"
    TOKEN_EXPIRE_SECONDS: int = 3600 * 24
    RESET_EXPIRE_SECONDS: int = 3600
    LOG_LEVEL: str = "DEBUG"


class ProdConfig(Config):
    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="PROD_", extra="ignore"
    )


@cache
def get_config(env: str = "dev") -> TestConfig | DevConfig | ProdConfig:
    return dict(test=TestConfig, dev=DevConfig, prod=ProdConfig)[env](ENV_STATE=env)


config = get_config(env=BaseConfig().ENV_STATE)
