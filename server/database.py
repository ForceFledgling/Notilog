from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

# Создание базы данных
Base = declarative_base()

# Настройка движка базы данных
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Инициализирует базу данных, создавая все таблицы, определенные в моделях.
    """
    from . import models  # Импорт моделей здесь для предотвращения циклического импорта
    Base.metadata.create_all(bind=engine)

def get_db():
    """
    Создает и закрывает сессию базы данных для каждого запроса.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
