from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Конфиг сервиса авторизации"""

    service_host: str = Field("localhost", env="SERVICE_HOST")
    service_port: int = Field("5000", env="SERVICE_PORT")
    debug: bool = Field(False, env="DEBUG")

    redis_host: str = Field("localhost", env="REDIS_HOST")
    redis_port: int = Field(6379, env="REDIS_PORT")

    jaeger_host: str = Field("localhost", env="JAEGER_HOST")
    jaeger_port: int = Field(6831, env="JAEGER_PORT")

    pg_host: str = Field("localhost", env="PG_HOST")
    pg_port: int = Field(5432, env="PG_PORT")
    pg_db_name: str = Field("auth_service_db", env="PG_DB_NAME")
    pg_user: str = Field(..., env="PG_USER")
    pg_pass: str = Field(..., env="PG_PASSWORD")

    # Ограничения количества запросов пользователей к сервису
    rate_limits = [
        "200 per day", # 200 запросов в день
        "50 per hour", # 50 запросов в час
        "1 per 10 second", # 1 запрос в 10 секунд
    ]

    class Config:
        env_file = "core/.env"
        env_file_encoding = "utf-8"


settings = Settings()
