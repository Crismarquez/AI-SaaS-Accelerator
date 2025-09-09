from __future__ import annotations

import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


def build_sqlite_url(file_name: str) -> str:
    data_dir = os.path.join(os.getcwd(), "data")
    os.makedirs(data_dir, exist_ok=True)
    return "sqlite:///" + os.path.join(data_dir, file_name)


def resolve_database_url(explicit_url: Optional[str], default_sqlite_file: str) -> str:
    if explicit_url:
        return explicit_url
    return build_sqlite_url(default_sqlite_file)


class SharedSettings(BaseSettings):
    app_env: str = "development"
    app_secret_key: str = "change-me"

    # Database
    database_url: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    def get_database_url(self, sqlite_file: str) -> str:
        return resolve_database_url(self.database_url, sqlite_file)


settings = SharedSettings()


