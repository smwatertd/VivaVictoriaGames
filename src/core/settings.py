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


class DatabaseSettings(BaseSettings):
    dialect: str = 'postgresql+asyncpg'
    options: str = '?async_fallback=true'

    host: str = 'localhost'
    port: int = 5432
    name: str = 'postgres'
    user: str = 'postgres'
    password: str = 'postgres'
    echo: bool = False

    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='DB_',
    )

    @property
    def url(self) -> str:
        return f'{self.dialect}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}{self.options}'


class GameSettings(BaseSettings):
    players_count_to_start: int = 3

    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='GAME_',
    )


app_settings = AppSettings()
redis_settings = RedisSettings()
db_settings = DatabaseSettings()
game_settings = GameSettings()
