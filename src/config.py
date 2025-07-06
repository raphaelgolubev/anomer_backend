from pathlib import Path

from pydantic import Field
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


class SecuritySettings(BaseSettings):
    secret_pem_file: Path = Field(alias='SECURITY_PRIVATE_JWT', default=Path('certs/jwt-private.pem'))
    public_pem_file: Path = Field(alias='SECURITY_PUBLIC_JWT', default=Path('certs/jwt-public.pem'))
    algorithm: str = Field(default='RS256')
    access_token_expire_minutes: int = 15
    refresh_token_expire_minutes: int = 30 * 24 * 60  # 30 дней

    model_config = ModelConfig(env_prefix='SECURITY_')


class ServerSettings(BaseSettings):
    host: str
    port: int

    model_config = ModelConfig(env_prefix='SERVER_')


class DatabaseSettings(BaseSettings):
    host: str
    port: int

    model_config = ModelConfig(env_prefix='DB_')


class AppSettings(BaseSettings):
    prefix: str = "/api"
    app_version: str = "0.0.1"


class Settings:
    app = AppSettings()
    security = SecuritySettings()
    server = ServerSettings()
    database = DatabaseSettings()


settings = Settings()
