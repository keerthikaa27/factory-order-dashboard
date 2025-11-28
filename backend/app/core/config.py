from dotenv import load_dotenv
import os
from pydantic import BaseModel
from typing import List

load_dotenv()


class Settings(BaseModel):
    APP_ENV: str = os.getenv("APP_ENV", "development")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./factory_dashboard.db")

    JWT_SECRET: str = os.getenv("JWT_SECRET", "changeme")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    )

    CORS_ALLOWED_ORIGINS: str = os.getenv(
        "CORS_ALLOWED_ORIGINS",
        "http://localhost:5173"
    )

    DATA_FOLDER: str = "data"
    IMAP_HOST: str | None = None
    IMAP_PORT: int = 993
    IMAP_USERNAME: str | None = None
    IMAP_PASSWORD: str | None = None
    IMAP_FOLDER: str = "INBOX"

    class Config:
        env_file = ".env"


settings = Settings()

# Safety check
if settings.APP_ENV == "production" and settings.JWT_SECRET == "changeme":
    raise ValueError("JWT_SECRET must be set in production")
