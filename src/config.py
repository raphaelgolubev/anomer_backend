from pydantic_settings import BaseSettings, SettingsConfigDict


class ModelConfig:
    """
    Определяет значения по умолчанию.
    Значения можно переопределять внутри класса `BaseSettings`:
    ```python
    class ExampleSettings(BaseSettings):
        ...
        model_config = ModelConfig(env_prefix='EXAMPLE_', env_file='example.dev.env')
    ```
    """
    def __new__(cls, *args, **kwargs):
        config = SettingsConfigDict(
            extra="ignore",
            validate_default=False,
            case_sensitive=False,
            env_ignore_empty=True,
            env_file_encoding='utf-8',
            env_file='.env'
        )
        config.update(**kwargs)
        return config


class ServerSettings(BaseSettings):
    host: str
    port: int

    model_config = ModelConfig(env_prefix='SERVER_')


class DatabaseSettings(BaseSettings):
    host: str
    port: int

    model_config = ModelConfig(env_prefix='DB_')


class Settings:
    server = ServerSettings()
    database = DatabaseSettings()


settings = Settings()

# Пример использования
# from config import settings
# print(settings.database.host)
