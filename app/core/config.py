from pydantic_settings import BaseSettings, SettingsConfigDict


class DataBaseSettings(BaseSettings):
    db_url: str
    echo: bool

    model_config = SettingsConfigDict(
        env_prefix='DATABASE_'
    )


class Settings(DataBaseSettings):

    model_config = SettingsConfigDict(
        env_file='.env'
    )


settings = Settings()
