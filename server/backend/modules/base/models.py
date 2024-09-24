import asyncio
from datetime import datetime
from sqlalchemy import select, func, Column, BigInteger, DateTime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

from backend.settings import settings
from backend.core.database import Base, SessionLocal


class BaseModel(Base):
    __abstract__ = True

    id = Column(BigInteger, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    @classmethod
    async def get(cls, id: int):
        async with SessionLocal() as s:
            result = await s.execute(select(cls).filter_by(id=id))
            return result.scalar_one_or_none()

    @classmethod
    def filter(cls, *args, **kwargs):
        return select(cls).filter_by(**kwargs)  # Возвращаем запрос, а не его результат
    
    @classmethod
    async def count_from_query(cls, query):
        async with SessionLocal() as session:
            result = await session.execute(select(func.count()).select_from(query))
            return result.scalar()

    async def to_dict(self, exclude_fields: list[str] | None = None):
        if exclude_fields is None:
            exclude_fields = []

        d = {}
        for column in self.__table__.columns:
            if column.name not in exclude_fields:
                value = getattr(self, column.name)
                if isinstance(value, datetime):
                    value = value.strftime(settings.DATETIME_FORMAT)
                d[column.name] = value
        return d
