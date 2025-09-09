from typing import Optional
import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    environment: str = "local"  # local | cloud
    database_url: Optional[str] = None
    cors_allowed_origins: str | None = None  # Comma-separated list

    # Firebase service account json path or json string
    firebase_credentials_file: Optional[str] = None
    firebase_project_id: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def sync_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        data_dir = os.path.join(os.getcwd(), "data")
        os.makedirs(data_dir, exist_ok=True)
        return "sqlite:///" + os.path.join(data_dir, "core_backend.db")

    @property
    def allowed_origins(self) -> list[str]:
        if not self.cors_allowed_origins:
            # Safe local default; restrict in production
            return ["http://localhost:3000", "http://127.0.0.1:3000"]
        return [o.strip() for o in self.cors_allowed_origins.split(",") if o.strip()]


settings = Settings()


