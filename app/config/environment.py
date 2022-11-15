import os
from functools import lru_cache

from pydantic import BaseSettings


@lru_cache
def get_env_filename():
    runtime_env = os.getenv("ENV")
    return f".env.{runtime_env}" if runtime_env else ".env"


class EnvironmentSettings(BaseSettings):
    API_VERSION: str = ""
    APP_NAME: str = ""
    DATABASE_DIALECT: str = ""
    DATABASE_HOSTNAME: str = ""
    DATABASE_NAME: str = ""
    DATABASE_PASSWORD: str = ""
    DATABASE_PORT: int = None
    DATABASE_USERNAME: str = ""
    DEBUG_MODE: bool = False
    MINUTES_PER_SESSION: float = 1000
    JWT_KEY: str = ""
    JWT_ENCRYPT_ALGO: str = "HS256"
    AWS_SES_ENDPOINT_URL: str = None
    AWS_REGION: str = None
    AWS_ACCESS_KEY: str = None
    AWS_SECRET_ACCESS_KEY: str = None

    class Config:
        env_file = get_env_filename()
        env_file_encoding = "utf-8"


API_VERSION = EnvironmentSettings().API_VERSION
APP_NAME = EnvironmentSettings().APP_NAME
DATABASE_DIALECT = EnvironmentSettings().DATABASE_DIALECT
DATABASE_HOSTNAME = EnvironmentSettings().DATABASE_HOSTNAME
DATABASE_NAME = EnvironmentSettings().DATABASE_NAME
DATABASE_PASSWORD = EnvironmentSettings().DATABASE_PASSWORD
DATABASE_PORT = EnvironmentSettings().DATABASE_PORT
DATABASE_USERNAME = EnvironmentSettings().DATABASE_USERNAME
DEBUG_MODE = EnvironmentSettings().DEBUG_MODE
MINUTES_PER_SESSION = EnvironmentSettings().MINUTES_PER_SESSION
JWT_KEY = EnvironmentSettings().JWT_KEY
JWT_ENCRYPT_ALGO = EnvironmentSettings().JWT_ENCRYPT_ALGO
AWS_SES_ENDPOINT_URL = EnvironmentSettings().AWS_SES_ENDPOINT_URL
AWS_REGION = EnvironmentSettings().AWS_REGION
AWS_ACCESS_KEY = EnvironmentSettings().AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = EnvironmentSettings().AWS_SECRET_ACCESS_KEY
