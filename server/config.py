from pydantic_settings import BaseSettings
from urllib.parse import quote_plus
class Settings(BaseSettings):
    DATABASE_HOST: str
    DATABASE_NAME: str
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str

    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_CHAT_ID: str

    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    EMAIL_HOST: str
    EMAIL_PORT: int

    SMTP_SERVER: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    EMAIL_FROM: str
    EMAIL_TO: str

    @property
    def DATABASE_URL(self) -> str:
        encoded_password = quote_plus(self.DATABASE_PASSWORD)  # URL-кодирование для пароля (исправляет проблемы, если пароль содержит спецсимволы)
        return f"postgresql+psycopg2://{self.DATABASE_USERNAME}:{encoded_password}@{self.DATABASE_HOST}:5432/{self.DATABASE_NAME}"

    class Config:
        env_file = ".env"

settings = Settings()
