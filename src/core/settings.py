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
    default_encoding: str = 'utf-8'
    pool_max_connections: int = 1

    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='REDIS_',
    )


class RabbitMQSettings(BaseSettings):
    host: str = 'localhost'
    port: int = 5672
    virtual_host: str = '/'
    exchange: str = 'games'

    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='RABBITMQ_',
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
    fields_count: int = 9
    max_rounds: int = 10
    duel_max_rounds: int = 3

    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='GAME_',
    )


class QuestionsSettings(BaseSettings):
    url: str = 'http://localhost:8000/api/questions'

    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='QUESTIONS_',
    )


app_settings = AppSettings()
redis_settings = RedisSettings()
rabbitmq_settings = RabbitMQSettings()
db_settings = DatabaseSettings()
game_settings = GameSettings()
questions_settings = QuestionsSettings()
