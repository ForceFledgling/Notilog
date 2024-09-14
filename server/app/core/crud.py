# server/app/core/crud.py

from typing import Any, Dict, Generic, List, NewType, Tuple, Type, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import sessionmaker

Total = NewType("Total", int)
BaseModelType = TypeVar("BaseModelType", bound="BaseModel")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

# Определение базового класса модели
@as_declarative()
class Base:
    id: int  # Замените на ваш реальный тип ID
    __name__: str

class CRUDBase(Generic[BaseModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[BaseModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get(self, id: int) -> BaseModelType:
        async with self.session() as session:
            return await session.execute(self.model.query().filter_by(id=id)).scalar_one()

    async def list(self, page: int, page_size: int, order: List[str] = []) -> Tuple[Total, List[BaseModelType]]:
        async with self.session() as session:
            query = self.model.query()
            total = await query.count()
            items = await query.offset((page - 1) * page_size).limit(page_size).order_by(*order).all()
            return total, items

    async def create(self, obj_in: CreateSchemaType) -> BaseModelType:
        async with self.session() as session:
            obj = self.model(**obj_in.dict())
            session.add(obj)
            await session.commit()
            return obj

    async def update(self, id: int, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> BaseModelType:
        async with self.session() as session:
            obj = await session.execute(self.model.query().filter_by(id=id)).scalar_one()
            for key, value in obj_in.items():
                setattr(obj, key, value)
            session.add(obj)
            await session.commit()
            return obj

    async def remove(self, id: int) -> None:
        async with self.session() as session:
            obj = await session.execute(self.model.query().filter_by(id=id)).scalar_one()
            session.delete(obj)
            await session.commit()
