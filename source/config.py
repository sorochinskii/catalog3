import pickle
import sys
from dataclasses import asdict, dataclass
from os import getenv

from dotenv import find_dotenv
from dump_env.dumper import dump
from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

TEMPLATE_ENV_FILE: str = '.env.template'
DEV_ENV_FILE: str = '.dev.env'
PROD_ENV_FILE: str = '.env'
LOCAL_ENV_FILE: str = '.dev.local.env'
LOCAL_TEST_ENV_FILE: str = '.local.testing.env'
TEST_ENV_FILE: str = '.testing.env'

ENVIRONMENT: str | None = getenv('ENVIRONMENT')


@dataclass
class EnvironmentVars:
    dev: str = 'dev'
    prod: str = 'prod'
    local: str = 'local'
    local_testing: str = 'local_testing'
    testing: str = 'testing'


print('environment', ENVIRONMENT)

match ENVIRONMENT:
    case EnvironmentVars.dev:
        env_file = find_dotenv(DEV_ENV_FILE, raise_error_if_not_found=True)
    case EnvironmentVars.prod:
        env_file = find_dotenv(TEST_ENV_FILE, raise_error_if_not_found=True)
    case EnvironmentVars.testing:
        env_file = find_dotenv(PROD_ENV_FILE, raise_error_if_not_found=True)
    case EnvironmentVars.local:
        variables = dump(template=TEMPLATE_ENV_FILE,
                         prefixes=['CATALOG3_'])
        with open(LOCAL_ENV_FILE, 'w') as file:
            for key, value in variables.items():
                file.write(f'{key}={value}\n')
        env_file = find_dotenv(LOCAL_ENV_FILE, raise_error_if_not_found=True)
    case EnvironmentVars.local_testing:
        variables = dump(template=TEMPLATE_ENV_FILE,
                         prefixes=['TESTING_CATALOG3_'])
        with open(TEST_ENV_FILE, 'w') as file:
            for key, value in variables.items():
                file.write(f'{key}={value}\n')
        env_file = find_dotenv(LOCAL_TEST_ENV_FILE,
                               raise_error_if_not_found=True)
    case _:
        raise Exception('Dot env file not found')


class Settings(BaseSettings):
    def __init__(self, env_file):
        super().__init__(_env_file=env_file, _case_sensitive=True, )

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
    V1: str = Field(default='v1')
    SECRET: str = Field(default='SECRET')
    TOKEN_LIFETIME: int | None = Field(default=None)
    TELEGRAM_TOKEN: str = Field(default='TELEGRAM_TOKEN')
    TELEGRAM_LOGIN: str = Field(default='TELEGRAM_LOGIN')
    SMTP_SERVER: str = Field(default='SMTP_SERVER')
    SENDER_EMAIL: str = Field(default='SMTP_SERVER')
    SENDER_PASSWORD: str = Field(default='SMTP_SERVER')
    SMTP_PORT: int = Field(default='123')
    TEMPLATES_DIR: str = Field(default='source/templates')
    TEMPLATE_VERIFICATION: str = Field(default='email_verification.html')
    HTTP_PROTOCOL: str = Field(default='https')
    HTTP_PORT: int | None = Field(default=None)

    @model_validator(mode='before')
    def get_database_url(cls, values):
        values['DB_URL'] = (
            f'postgresql+asyncpg://{values["DB_USER"]}:{values["DB_PASS"]}'
            + f'@{values["DB_HOST"]}:{values["DB_PORT"]}/{values["DB_NAME"]}'
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
