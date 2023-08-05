import os
from enum import Enum
from dotenv import load_dotenv
from pydantic import BaseModel, BaseSettings, root_validator
from typing import Optional

from app.constants import EnvironmentHandler


load_dotenv()

PROJECT_NAME = 'mailing_service'
PROJECT_NAME_SLUG = 'mailing_service'

ENVIRONMENT = EnvironmentHandler.get_environment_name(os.environ.get('ENVIRONMENT', 'LOCAL'))


class OrmEnum(str, Enum):
    alchemy = "alchemy"
    tortoise = "tortoise"


class BaseHealthCheckSettings(BaseModel):
    ENABLED: bool = False


class HealthCheckPostgresSettings(BaseHealthCheckSettings):
    ORM: Optional[OrmEnum]

    @root_validator(pre=True)
    def check_config(cls, values: dict) -> dict:
        if values.get("ENABLED") and not values.get("ORM"):
            raise ValueError("ORM is not set")
        return values


class InternalRouterSettings(BaseHealthCheckSettings):
    ENABLED: bool = True
    PATH: str = "/api/internal/v1/healthcheck"


class ExternalRouterSeiitngs(BaseHealthCheckSettings):
    PATH: str = "/api/public/v1/healthcheck"


class HealthCheckSettings(BaseSettings):
    """
    HEALTH_CHECKS__DB__ENABLED=1
    HEALTH_CHECKS__DB__ORM="tortoise"
    """

    ENABLED: bool = True
    POSTGRES: Optional[HealthCheckPostgresSettings] = HealthCheckPostgresSettings()
    INTERNAL: InternalRouterSettings = InternalRouterSettings()
    EXTERNAL: ExternalRouterSeiitngs = ExternalRouterSeiitngs()  # noqa CCE001

    class Config:
        env_prefix = "HEALTH_CHECKS__"
        use_enum_values = True
        env_nested_delimiter = "__"


class LoggingSettings(BaseSettings):
    class Config:
        env_file = ".env"

    service_name: str
    log_level: str = "INFO"
    log_as_json: bool = True


class UvicornConfig(BaseSettings):
    class Config:
        env_prefix = "uvicorn_"
        env_file = ".env"

    app: str = "app.main:app"
    host: str = "0.0.0.0"  # nosec
    port: int = 5000
    log_level: str = "info"
    reload: bool = False
    limit_max_requests: Optional[int] = None


class ApiSettings(BaseSettings):
    class Config:
        env_prefix = 'API_'

    ROOT: str = '/api'
    DOCS_ENABLED: bool = True
    VERSION: str = '0.1'


class DatabaseSettings(BaseSettings):
    class Config:
        env_prefix = 'SQL_'
        env_file = '.env'

    HOST: str
    USER: str
    PASSWORD: str
    PORT: int
    PROTOCOL: str = 'postgresql+asyncpg'
    DATABASE: str
    TIMEOUT_CONNECTION: float = 15
    TIMEOUT_COMMAND: float = 60
    MIGRATION_TIMEOUT_COMMAND: float = 600
    POOL_RECYCLE: int = 1800

    SCHEMA: str = 'content'


class Settings(LoggingSettings):
    LOG_LEVEL: str = 'INFO'
    API: ApiSettings = ApiSettings()
    UVICORN: UvicornConfig = UvicornConfig()
    DB: DatabaseSettings = DatabaseSettings()
    ENVIRONMENT = ENVIRONMENT
    service_name: str = f'{PROJECT_NAME}'


SETTINGS: Settings = Settings()
