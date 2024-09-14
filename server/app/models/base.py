import asyncio
from datetime import datetime

from tortoise import fields, models

from app.settings import settings


from sqlalchemy.ext.declarative import declarative_base


# Base = declarative_base()
from app.core.database import Base


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, DateTime
from sqlalchemy.sql import func
from app.core.database import SessionLocal
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

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



class UUIDModel:
    uuid = fields.UUIDField(unique=True, pk=False, index=True)


class TimestampMixin:
    created_at = fields.DatetimeField(auto_now_add=True, index=True)
    updated_at = fields.DatetimeField(auto_now=True, index=True)
