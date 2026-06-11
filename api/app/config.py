from typing import Annotated

from pydantic import field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    """Configuration read from the environment (12-factor)."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str
    # NoDecode skips pydantic-settings' default JSON parsing so the validator below
    # can read a plain comma-separated string (e.g. "http://a,http://b").
    cors_allow_origins: Annotated[list[str], NoDecode] = []
    db_readiness_timeout_seconds: float = 2.0

    @field_validator("cors_allow_origins", mode="before")
    @classmethod
    def split_comma_separated_origins(cls, value: object) -> object:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value
