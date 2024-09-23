from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from .models import Event
from .schemas import EventCreate, EventUpdate


class EventController:
    async def get(self, session: AsyncSession, id: int):
        """
        Получение события по ID.
        """
        query = select(Event).filter(Event.id == id)
        result = await session.execute(query)
        event = result.scalars().first()

        # Если событие не найдено, возвращаем None
        if event is None:
            return None

        return jsonable_encoder(event)

    async def get_all(self, session: AsyncSession, skip: int = 0, limit: int = 10):
        query = select(Event).offset(skip).limit(limit)
        result = await session.execute(query)
        events = result.scalars().all()
        return jsonable_encoder(events)


    async def count(self, session: AsyncSession):
        """
        Подсчет общего количества событий.
        """
        query = select(func.count(Event.id))
        result = await session.execute(query)
        return result.scalar()

    async def create(self, session: AsyncSession, obj_in: EventCreate):
        """
        Создание нового события.
        """
        new_event = Event(**obj_in.dict())
        session.add(new_event)
        await session.commit()
        await session.refresh(new_event)
        return new_event

    async def update(self, session: AsyncSession, id: int, obj_in: EventUpdate):
        """
        Обновление существующего события.
        """
        query = select(Event).filter(Event.id == id)
        result = await session.execute(query)
        event = result.scalars().first()

        if event:
            for key, value in obj_in.dict(exclude_unset=True).items():
                setattr(event, key, value)
            await session.commit()
            await session.refresh(event)
        return event

    async def remove(self, session: AsyncSession, id: int):
        """
        Удаление события по ID.
        """
        query = select(Event).filter(Event.id == id)
        result = await session.execute(query)
        event = result.scalars().first()

        if event:
            await session.delete(event)
            await session.commit()
        return event


# Экземпляр контроллера
event_controller = EventController()
