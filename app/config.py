from typing import Literal

from pydantic_settings import BaseSettings

# from pydantic import model_validator


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    TEST_DB_PORT: int
    TEST_DB_HOST: str
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    ALGORITHM: str
    SECRET_KEY: str

    SMTP_HOST: str
    SMTP_PORT: str
    SMTP_USER: str
    SMTP_PASS: str

    BROKER_CELERY: str

    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", ]
    # @model_validator(skip_on_failure=True)
    # def get_database_url(cls, v):
    #     v["DATABASE_URL"] = f"postgresql+asyncpg://{v['DB_USER']}:{v['DB_PASS']}@{v['DB_HOST']}:{v['DB_PORT']}/{v['DB_NAME']}"
    #     return v

    class Config:
        env_file = ".env"


settings = Settings()
# settings.DAT
# print(settings.DB_HOST)
