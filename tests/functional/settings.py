from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Конфиг для тестов сервиса авторизации"""

    redis_host: str = Field('localhost', env="REDIS_HOST")
    redis_port: int = Field(6379, env="REDIS_PORT")

    pg_host: str = Field('localhost', env="PG_HOST")
    pg_port: int = Field(5432, env="PG_PORT")
    pg_db_name: str = Field('auth_service_db', env="PG_DB_NAME")
    pg_user: str = Field('app', env="PG_USER")
    pg_pass: str = Field('123qwe', env="PG_PASSWORD")

    service_url: str = Field("http://localhost:5001", env="FLASK_URL")

    class Config:
        env_file = "tests/functional/.env"
        env_file_encoding = "utf-8"


test_settings = Settings()
