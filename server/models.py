from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from .database import Base


class Event(Base):
    """
    Представляет модель события в базе данных.

    Эта модель определяет структуру таблицы `events`, которая хранит информацию о различных событиях в системе.
    Каждое событие имеет уникальный идентификатор, заголовок, описание, уровень важности и временную метку.

    Attributes:
        id (int): Уникальный идентификатор события. Первичный ключ.
        title (str): Заголовок события. Используется для краткого описания события.
        description (str): Полное описание события, содержащее все необходимые детали.
        level (str): Уровень важности события (например, "INFO", "WARNING", "ERROR").
        timestamp (datetime): Время создания события. По умолчанию устанавливается текущее время.

    Таблица:
        __tablename__ (str): Имя таблицы в базе данных, в которой хранятся записи событий.
    """
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    level = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
