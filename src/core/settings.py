from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    name: str = 'FastAPI'
    host: str = '0.0.0.0'
    port: int = 8000

    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='APP_',
    )


class RedisSettings(BaseSettings):
    host: str = 'localhost'
    port: int = 6379
    db: int = 0

    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='REDIS_',
    )


class PostgresSettings(BaseSettings):
    host: str = 'localhost'
    port: int = 5432
    db: str = 'games'
    user: str = 'me'
    password: str = '5'


app_settings = AppSettings()
redis_settings = RedisSettings()
postgres_settings = PostgresSettings()
