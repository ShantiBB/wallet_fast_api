from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class DataBaseSettings(BaseModel):
    user: str
    password: str
    host: str
    port: str
    name: str
    echo: bool

    @property
    def sync_url(self):
        """Формирует путь для настройки синхронной БД"""
        return (
            f'postgresql+psycopg2://{self.user}:{self.password}'
            f'@{self.host}:{self.port}/{self.name}'
        )

    @property
    def async_url(self):
        """Формирует путь для настройки асинхронной БД"""
        return (
            f'postgresql+asyncpg://{self.user}:{self.password}'
            f'@{self.host}:{self.port}/{self.name}'
        )


class AccessTokenSettings(BaseModel):
    reset_password_token_secret: str
    verification_token_secret: str
    lifetime_seconds: int


class CelerySettings(BaseModel):
    rabbitmq_host: str
    redis_host: str

    @property
    def setup_celery_config(self):
        """Формирует настройки Celery на основе переменных окружения"""
        return {
            "broker_url": f"pyamqp://guest@{self.rabbitmq_host}//",
            "result_backend": f"redis://{self.redis_host}:6379/1",
            "task_serializer": "json",
            "result_serializer": "json",
            "accept_content": ["application/json"],
            "timezone": "UTC",
            "broker_transport_options": {"visibility_timeout": 3600},
            "broker_connection_retry_on_startup": True,
        }


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_nested_delimiter = '__'
    )

    postgres: DataBaseSettings
    access_token: AccessTokenSettings
    celery: CelerySettings


settings = Settings()
