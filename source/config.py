import sys
from dataclasses import asdict, dataclass
from os import getenv

from dotenv import find_dotenv
from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

DEV_ENV_FILE: str = '.dev.env'
PROD_ENV_FILE: str = '.env'
LOCAL_ENV_FILE: str = '.dev.local.env'
TEST_ENV_FILE: str = '.testing.env'
ENVIRONMENT: str | None = getenv('ENVIRONMENT')


@dataclass
class EnvironmentVars:
    dev: str = 'dev'
    prod: str = 'prod'
    local: str = 'local'
    testing: str = 'testing'


print('environment', ENVIRONMENT)

match ENVIRONMENT:
    case EnvironmentVars.dev:
        env_file = find_dotenv(DEV_ENV_FILE, raise_error_if_not_found=True)
    case EnvironmentVars.prod:
        env_file = find_dotenv(PROD_ENV_FILE, raise_error_if_not_found=True)
    case EnvironmentVars.local:
        env_file = find_dotenv(LOCAL_ENV_FILE, raise_error_if_not_found=True)
    case EnvironmentVars.testing:
        env_file = find_dotenv(TEST_ENV_FILE, raise_error_if_not_found=True)
    case _:
        raise Exception('Dot env file not found')


class Settings(BaseSettings):
    def __init__(self, env_file):
        super().__init__(_env_file=env_file, _case_sensitive=True)

    DB_HOST: str = Field(default='DB_HOST')
    DB_PASS: str = Field(default='DB_PASS')
    DB_PORT: str = Field(default='DB_PORT')
    DB_USER: str = Field(default='DB_USER')
    DB_NAME: str = Field(default='DB_NAME')
    DB_URL: str = Field(default='DB_URL')
    POSTGRES_PASSWORD: str = Field(default='POSTGRES_PASSWORD')
    POSTGRES_USER: str = Field(default='POSTGRES_USER')
    POSTGRES_DB: str = Field(default='POSTGRES_DB')
    DB_ENGINE: str = Field(default='DB_ENGINE')
    HOST: str = Field(default='localhost')
    SECRET_KEY: str = Field(default='SECRET_KEY')
    SSH_KEY: str = Field(default='SSH_KEY')
    SSH_PASSPHRASE: str = Field(default='SSH_PASSPHRASE')
    SSH_PORT: str = Field(default='SSH_PORT')
    USER: str = Field(default='USER')
    PROJECT_NAME: str = Field(default='PROJECT_NAME')
    ENVIRONMENT: str = Field(default='ENVIRONMENT')
    LOG_DIR: str = Field(default='logs')
    HTTP_PORT: int = Field(default=8445)
    V1: str = Field(default='v1')

    @model_validator(mode='before')
    def get_database_url(cls, values):
        values['DB_URL'] = (
            f"postgresql+asyncpg://{values['DB_USER']}:{values['DB_PASS']}"
            + f"@{values['DB_HOST']}:{values['DB_PORT']}/{values['DB_NAME']}"
        )
        return values

    @model_validator(mode='after')
    def set_environment(self):
        env_vars = EnvironmentVars()
        assert self.ENVIRONMENT in asdict(env_vars).values(), \
            f'{self.ENVIRONMENT=} not in possible {asdict(env_vars).values()}'
        return self

    class Config:
        validate_assignment = True


settings = Settings(env_file=env_file)
