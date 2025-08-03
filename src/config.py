from pathlib import Path

from pydantic import Field, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class ModelConfig:
    """
    Определяет значения по умолчанию.
    Значения можно переопределять внутри наследника `BaseSettings`:
    ```python
    class ExampleSettings(BaseSettings):
        ...
        model_config = ModelConfig(env_prefix="EXAMPLE_", env_file="example.dev.env")
    ```
    """

    def __new__(cls, *args, **kwargs):
        config = SettingsConfigDict(
            extra="ignore",
            validate_default=False,
            case_sensitive=False,
            env_ignore_empty=True,
            env_file_encoding="utf-8",
            env_file=".env",
        )
        config.update(**kwargs)
        return config


class ApiV1Config(BaseModel):
    prefix: str = "/v1"
    auth: str = "/auth"
    users: str = "/users"


class SecuritySettings(BaseSettings):
    secret_pem_file: Path = Field(
        alias="SECURITY_PRIVATE_JWT", default=Path("certs/jwt-private.pem")
    )
    public_pem_file: Path = Field(
        alias="SECURITY_PUBLIC_JWT", default=Path("certs/jwt-public.pem")
    )
    algorithm: str = Field(default="RS256")
    access_token_expire_minutes: int = 15
    refresh_token_expire_minutes: int = 30 * 24 * 60  # 30 дней

    model_config = ModelConfig(env_prefix="SECURITY_")


class ServerSettings(BaseSettings):
    host: str
    port: int

    model_config = ModelConfig(env_prefix="SERVER_")


class DatabaseSettings(BaseSettings):
    user: str
    password: str
    name: str
    port: int
    host: str

    @property
    def async_dsn(self):
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_conventions: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    model_config = ModelConfig(env_prefix="DB_")



class MailSettings(BaseSettings):
    port: int = 465
    hostname: str
    password: str
    sender: str
    templates_path: Path

    model_config = ModelConfig(env_prefix="MAIL_")


class RedisSettings(BaseSettings):
    host: str = "localhost"
    port: int = 6379
    db: int = 0
    username: str | None = None
    password: str | None = None
    verification_code_ttl: int = 300  # 5 минут в секундах

    model_config = ModelConfig(env_prefix="REDIS_")


class AppSettings(BaseSettings):
    name: str = "Anomer"
    app_version: str = "0.0.1"
    prefix: str = "/api"
    v1: ApiV1Config = ApiV1Config()


class Settings:
    app = AppSettings()
    security = SecuritySettings()
    server = ServerSettings()
    db = DatabaseSettings()
    mail = MailSettings()
    redis = RedisSettings()


settings = Settings()
