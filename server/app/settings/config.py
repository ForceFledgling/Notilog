import os
import typing
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    VERSION: str = "0.1"
    APP_TITLE: str = "NotiLog CPanel"
    PROJECT_NAME: str = "NotiLog CPanel"
    APP_DESCRIPTION: str = "Description"

    CORS_ORIGINS: typing.List[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: typing.List[str] = ["*"]
    CORS_ALLOW_HEADERS: typing.List[str] = ["*"]

    DEBUG: bool = True
    DB_URL: str = os.getenv("DB_URL", "sqlite://db.sqlite3")  # По умолчанию SQLite
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")  # Указывается в .env
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")  # По умолчанию HS256
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 24 * 7))  # По умолчанию  7 дней

    DB_CONNECTIONS: dict = {
        "default": {
            "engine": "tortoise.backends.sqlite",
            "db_url": DB_URL,
            "credentials": {
                "host": "",
                "port": "",
                "user": "",
                "password": "",
                "database": "",
            },
        },
    }

    PROJECT_ROOT: str = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    BASE_DIR: str = os.path.abspath(os.path.join(PROJECT_ROOT, os.pardir))
    LOGS_ROOT: str = os.path.join(BASE_DIR, "app/logs")

    TORTOISE_ORM: dict = {
        "connections": {
            "sqlite": {
                "engine": "tortoise.backends.sqlite",
                "credentials": {"file_path": f"{BASE_DIR}/db.sqlite3"},
            }
        },
        "apps": {
            "models": {
                "models": ["app.models"],
                "default_connection": "sqlite",
            },
        },
        "use_tz": False,
        "timezone": "Europe/Moscow",
    }
    DATETIME_FORMAT: str = "%Y-%m-%d %H:%M:%S"

    class Config:
        env_file = ".env"  # Указываем, что переменные загружаются из .env файла


settings = Settings()
