from os import getenv

from dotenv import find_dotenv
from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

DEV_ENV_FILE: str = ".dev.env"
PROD_ENV_FILE: str = ".env"
LOCAL_ENV_FILE: str = ".dev.local.env"
ENVIRONMENT: str | None = getenv("ENVIRONMENT")


class Settings(BaseSettings):
    def __init__(self, env_file):
        super().__init__(_env_file=env_file, _case_sensitive=True)

    DB_HOST: str = Field(default="DB_HOST")
    DB_PASS: str = Field(default="DB_PASS")
    DB_PORT: str = Field(default="DB_PORT")
    DB_USER: str = Field(default="DB_USER")
    DB_NAME: str = Field(default="DB_NAME")
    DB_URL: str = Field(default="DB_URL")
    POSTGRES_PASSWORD: str = Field(default="POSTGRES_PASSWORD")
    POSTGRES_USER: str = Field(default="POSTGRES_USER")
    POSTGRES_DB: str = Field(default="POSTGRES_DB")
    DB_ENGINE: str = Field(default="DB_ENGINE")
    HOST: str = Field(default="HOST")
    SECRET_KEY: str = Field(default="SECRET_KEY")
    SSH_KEY: str = Field(default="SSH_KEY")
    SSH_PASSPHRASE: str = Field(default="SSH_PASSPHRASE")
    SSH_PORT: str = Field(default="SSH_PORT")
    USER: str = Field(default="USER")
    PROJECT_NAME: str = Field(default="PROJECT_NAME")
    ENVIRONMENT: str = Field(default="ENVIRONMENT")

    @model_validator(mode="before")
    def get_database_url(cls, v):
        v["DB_URL"] = (
            f"postgresql+asyncpg://{v['DB_USER']}:{v['DB_PASS']}"
            + f"@{v['DB_HOST']}:{v['DB_PORT']}/{v['DB_NAME']}"
        )
        return v


match ENVIRONMENT:
    case "dev":
        env_file = find_dotenv(DEV_ENV_FILE, raise_error_if_not_found=True)
    case "prod":
        env_file = find_dotenv(PROD_ENV_FILE, raise_error_if_not_found=True)
    case "local":
        env_file = find_dotenv(LOCAL_ENV_FILE, raise_error_if_not_found=True)
    case None:
        raise Exception("dot env file not found")

settings = Settings(env_file=env_file)
