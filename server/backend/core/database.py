from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from backend.settings.config import settings

Base = declarative_base()

# Настройка подключения к базе данных
DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL

# Создание асинхронного двигателя и сессии
engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

def get_session() -> AsyncSession:
    return SessionLocal()