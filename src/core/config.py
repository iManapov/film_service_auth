from typing import Any

from pydantic import BaseSettings, Field
import enum


class Settings(BaseSettings):
    """Конфиг сервиса авторизации"""

    service_host: str = Field("localhost", env="SERVICE_HOST")
    service_port: int = Field("5000", env="SERVICE_PORT")
    debug: bool = Field(True, env="DEBUG")
    sentry_dsn: str = Field(..., env='SENTRY_DSN')

    redis_host: str = Field("localhost", env="REDIS_HOST")
    redis_port: int = Field(6379, env="REDIS_PORT")

    enable_tracer: bool = Field(True, env="ENABLE_TRACER")
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


class YandexSettings(BaseSettings):
    id: str = Field("", env="YANDEX_ID")
    secret: str = Field("", env="YANDEX_SECRET")
    authorize_url: str = Field("https://oauth.yandex.ru/authorize")
    access_token_url: str = Field("https://oauth.yandex.ru/token")
    base_url: str = Field("https://oauth.yandex.ru/")

    class Config:
        env_file = "core/.env"
        env_file_encoding = "utf-8"


class VkSettings(BaseSettings):
    id: str = Field("", env="VK_ID")
    secret: str = Field("", env="VK_SECRET")
    authorize_url: str = Field("https://oauth.vk.com/authorize")
    access_token_url: str = Field("https://oauth.vk.com/access_token")
    base_url: str = Field("https://oauth.vk.com/")

    class Config:
        env_file = "core/.env"
        env_file_encoding = "utf-8"


class GoogleSettings(BaseSettings):
    id: str = Field("", env="GOOGLE_ID")
    secret: str = Field("", env="GOOGLE_SECRET")
    authorize_url: str = Field("https://accounts.google.com/o/oauth2/v2/auth")
    access_token_url: str = Field("https://oauth2.googleapis.com/token")
    base_url: str = Field("https://accounts.google.com/")

    class Config:
        env_file = "core/.env"
        env_file_encoding = "utf-8"


class MailSettings(BaseSettings):
    id: str = Field("", env="MAIL_ID")
    secret: str = Field("", env="MAIL_SECRET")
    authorize_url: str = Field("https://connect.mail.ru/oauth/authorize")
    access_token_url: str = Field("https://connect.mail.ru/oauth/token")
    base_url: str = Field("https://connect.mail.ru")
    private_key: str = Field("", env="MAIL_PRIVATE")

    class Config:
        env_file = "core/.env"
        env_file_encoding = "utf-8"

# class ProvidersSettings(BaseSettings):
#     def __init__(self, provider, **values: Any):
#         super().__init__(**values)
#         provider = provider.upper()
#         self.id: str = Field(..., env=f"{provider}_ID")
#         secret: str = Field(..., env=f"{provider}_SECRET")
#         authorize_url: str = Field(..., env=f"{provider}_AUTH_URL")
#         access_token_url: str = Field(..., env=f"{provider}_TOKEN_URL")
#         base_url: str = Field(..., env=f"{provider}_BASE_URL")
#
#     class Config:
#         env_file = "core/.env"
#         env_file_encoding = "utf-8"


class Providers(enum.Enum):
    yandex = 1
    vk = 2
    google = 3
    mail = 4


settings = Settings()
yandex = YandexSettings()
vk = VkSettings()
google = GoogleSettings()
mail = MailSettings()
# vk = ProvidersSettings(Providers.vk.name)

