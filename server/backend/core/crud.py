from typing import Any, Dict, Generic, List, NewType, Tuple, Type, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import as_declarative
from sqlalchemy import func


from backend.core.database import SessionLocal

Total = NewType("Total", int)
BaseModelType = TypeVar("BaseModelType", bound=BaseModel)
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
        self.session = SessionLocal

    async def get(self, id: int) -> BaseModelType:
        async with self.session() as session:
            stmt = select(self.model).filter_by(id=id)
            result = await session.execute(stmt)
            return result.scalars().first()

    async def list(self, page: int, page_size: int, order: List[str] = [], **filters) -> Tuple[int, List[BaseModelType]]:
        async with self.session() as session:
            # Применение фильтров
            stmt = select(self.model).filter_by(**filters)
            
            # Получение общего количества записей
            total_stmt = select(func.count()).select_from(stmt.subquery())
            total_result = await session.execute(total_stmt)
            total = total_result.scalar()

            # Получение страниц с сортировкой
            stmt = stmt.order_by(*order).offset((page - 1) * page_size).limit(page_size)
            items_result = await session.execute(stmt)
            items = items_result.scalars().all()

            return total, items

    async def create(self, obj_in: CreateSchemaType) -> BaseModelType:
        async with self.session() as session:
            obj = self.model(**obj_in.dict(exclude_unset=True))  # Используем exclude_unset=True
            session.add(obj)
            await session.commit()
            return obj

    async def update(self, id: int, obj_in: Union[UpdateSchemaType, Dict[str, Any]]) -> BaseModelType:
        async with self.session() as session:
            stmt = select(self.model).filter_by(id=id)
            result = await session.execute(stmt)
            obj = result.scalars().first()
            if obj is None:
                raise ValueError("Object not found")
            for key, value in obj_in.items():
                setattr(obj, key, value)
            session.add(obj)
            await session.commit()
            return obj

    async def remove(self, id: int) -> None:
        async with self.session() as session:
            # Создание запроса для поиска объекта по ID
            stmt = select(self.model).filter_by(id=id)
            result = await session.execute(stmt)
            
            # Получение первого объекта из результата запроса
            obj = result.scalars().first()
            
            # Проверка, существует ли объект
            if obj is None:
                raise ValueError("Object not found")
            
            # Удаление объекта
            await session.delete(obj)
            
            # Коммит изменений в базе данных
            await session.commit()

