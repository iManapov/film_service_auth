from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Конфиг сервиса авторизации"""

    redis_host: str = Field('localhost', env="REDIS_HOST")
    redis_port: int = Field(6379, env="REDIS_PORT")

    pg_host: str = Field('localhost', env="PG_HOST")
    pg_port: int = Field(5432, env="PG_PORT")
    pg_db_name: str = Field('auth_service_db', env="PG_DB_NAME")
    pg_user: str = Field(..., env="PG_USER")
    pg_pass: str = Field(..., env="PG_PASSWORD")

    class Config:
        env_file = "src/core/.env"
        env_file_encoding = "utf-8"


settings = Settings()
