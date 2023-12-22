from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    name: str = 'FastAPI'
    host: str = '0.0.0.0'
    port: int = 8000

    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='APP_',
    )


class GameMessageBrokerSettings(BaseSettings):
    host: str = 'localhost'
    port: int = 6379
    db: int = 0
    encoding: str = 'utf-8'

    model_config = SettingsConfigDict(
        env_file='.env',
        env_prefix='GAME_MESSAGE_BROKER_',
    )


class GameEventMessageBrokerSettings(BaseSettings):
    host: str = 'localhost'
    port: int = 5672
    virtual_host: str = '/'
    exchange: str = 'games'
    games_events_queue: str = 'games.events'

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
    players_count_to_start: int = 2
    fields_count: int = 9
    max_rounds: int = 2
    duel_max_rounds: int = 3
    round_time_seconds: int = 30
    duel_round_time_seconds: int = 15

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
game_message_broker_settings = GameMessageBrokerSettings()
game_events_message_broker_settings = GameEventMessageBrokerSettings()
db_settings = DatabaseSettings()
game_settings = GameSettings()
questions_settings = QuestionsSettings()
