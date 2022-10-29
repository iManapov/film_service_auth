from pydantic import BaseSettings, Field, PostgresDsn


class TestSettings(BaseSettings):
    """Конфиг тестов"""

    redis_host: str = Field("0.0.0.0", env="REDIS_HOST")
    redis_port: int = Field(6379, env="REDIS_PORT")

    pg_dsn: PostgresDsn = 'postgres://{user}:{password}@{host}:{port}/{dbname}'.format(user=Field('app', env="DB_USER"),
                                                                                       password=Field('123qwe', env="DB_PASSWORD"),
                                                                                       host=Field('localhost', env="DB_HOST"),
                                                                                       port=Field('5432', env="DB_PORT"),
                                                                                       dbname=Field('movies_database', env="DB_NAME"))
    service_url: str = Field("http://localhost:5000", env="FAST_API_URL")

    class Config:
        env_file = "tests/functional/.env"
        env_file_encoding = "utf-8"


test_settings = TestSettings()
