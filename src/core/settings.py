import pydantic
import pydantic_settings


class BaseSettings(pydantic_settings.BaseSettings):
    model_config = pydantic_settings.SettingsConfigDict(
        env_nested_delimiter="__", env_file=".env", use_enum_values=True, extra="ignore"
    )


class SystemSettings(BaseSettings):
    x_api_key: str = pydantic.Field(default="salt-api-key")


class ServerSettings(pydantic.BaseModel):
    port: int = pydantic.Field(default=8000)
    workers: pydantic.PositiveInt = pydantic.Field(default=1)
    reload: bool = pydantic.Field(default=True)
    root_path: str = pydantic.Field(default="")


class DatabaseSettings(pydantic.BaseModel):
    dsn: pydantic.PostgresDsn
    engine_pool_size: int = pydantic.Field(default=20)
    engine_max_overflow: int = pydantic.Field(default=0)
    engine_pool_ping: bool = pydantic.Field(default=False)
    engine_pool_timeout: int = pydantic.Field(default=30)


class BrokerSettings(pydantic.BaseModel):
    dsn: pydantic.AmqpDsn


class APISettings(BaseSettings):
    system: SystemSettings
    server: ServerSettings
    database: DatabaseSettings


class ConsumerSettings(BaseSettings):
    database: DatabaseSettings
    broker: BrokerSettings


class WorkerSettings(BaseSettings):
    database: DatabaseSettings
    broker: BrokerSettings
