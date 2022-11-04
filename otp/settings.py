import os
from typing import Optional

import sentry_sdk
from pydantic import BaseSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TFA_ICON_DIR = os.path.join(BASE_DIR, "static", "tfa")
DEFAULT_ICON_PATH = os.path.join(TFA_ICON_DIR, "tfa.svg")
JWT_ALGORITHM = "HS256"
TFA_JSON_URL = "https://2fa.directory/api/v3/tfa.json"
TFA_JSON_PATH = os.path.join(TFA_ICON_DIR, "tfa.json")


class Settings(BaseSettings):
    DEBUG: bool = False
    DB_URL: str
    SECRET: str
    ENV = "production"
    SENTRY_DSN: Optional[str]
    WECHAT_APP_ID: str
    WECHAT_APP_SECRET: str

    class Config:
        env_file = ".env"


settings = Settings()  # type: ignore

TORTOISE_ORM = {
    "apps": {
        "models": {
            "models": ["otp.models", "aerich.models"],
            "default_connection": "default",
        },
    },
    "connections": {"default": settings.DB_URL},
}
sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    environment=settings.ENV,
    traces_sample_rate=1.0,
)
