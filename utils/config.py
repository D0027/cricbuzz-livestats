"""
Central application configuration.

Loads settings from environment variables (via a .env file) and exposes
them as a validated, typed Settings object. All other modules should
import `settings` from here instead of reading os.environ directly.
"""
from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class Settings(BaseModel):
    """Typed application settings."""

    # Cricbuzz API
    cricbuzz_api_key: str = Field(default_factory=lambda: os.getenv("CRICBUZZ_API_KEY", ""))
    cricketdata_api_key: str = os.getenv("CRICKETDATA_API_KEY", "")
    cricbuzz_api_host: str = Field(
        default_factory=lambda: os.getenv("CRICBUZZ_API_HOST", "cricbuzz-cricket.p.rapidapi.com")
    )
    cricbuzz_base_url: str = Field(
        default_factory=lambda: os.getenv(
            "CRICBUZZ_BASE_URL", "https://cricbuzz-cricket.p.rapidapi.com"
        )
    )

    # Database
    db_type: str = Field(default_factory=lambda: os.getenv("DB_TYPE", "sqlite"))
    db_path: str = Field(default_factory=lambda: os.getenv("DB_PATH", "data/cricbuzz.db"))
    db_host: str = Field(default_factory=lambda: os.getenv("DB_HOST", "localhost"))
    db_port: str = Field(default_factory=lambda: os.getenv("DB_PORT", "3306"))
    db_name: str = Field(default_factory=lambda: os.getenv("DB_NAME", "cricbuzz_livestats"))
    db_user: str = Field(default_factory=lambda: os.getenv("DB_USER", "root"))
    db_password: str = Field(default_factory=lambda: os.getenv("DB_PASSWORD", ""))

    # App
    app_env: str = Field(default_factory=lambda: os.getenv("APP_ENV", "development"))
    log_level: str = Field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    cache_ttl_seconds: int = Field(
        default_factory=lambda: int(os.getenv("CACHE_TTL_SECONDS", "60"))
    )
    request_timeout: int = Field(default_factory=lambda: int(os.getenv("REQUEST_TIMEOUT", "10")))
    request_max_retries: int = Field(
        default_factory=lambda: int(os.getenv("REQUEST_MAX_RETRIES", "3"))
    )

    @property
    def sqlalchemy_url(self) -> str:
        """Build the SQLAlchemy connection string for the configured DB type."""
        if self.db_type == "sqlite":
            db_full_path = BASE_DIR / self.db_path
            db_full_path.parent.mkdir(parents=True, exist_ok=True)
            return f"sqlite:///{db_full_path}"
        if self.db_type == "mysql":
            return (
                f"mysql+pymysql://{self.db_user}:{self.db_password}"
                f"@{self.db_host}:{self.db_port}/{self.db_name}"
            )
        if self.db_type == "postgresql":
            return (
                f"postgresql+psycopg2://{self.db_user}:{self.db_password}"
                f"@{self.db_host}:{self.db_port}/{self.db_name}"
            )
        raise ValueError(f"Unsupported DB_TYPE: {self.db_type}")

    @property
    def api_configured(self) -> bool:
        return bool(self.cricbuzz_api_key) and self.cricbuzz_api_key != "your_rapidapi_key_here"
    @property
    def cricketdata_configured(self) -> bool:
        return bool(self.cricketdata_api_key.strip())


settings = Settings()
