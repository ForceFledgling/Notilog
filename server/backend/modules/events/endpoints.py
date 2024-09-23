from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from backend.core.database import SessionLocal, get_session
from backend.modules.base.schemas import Fail, Success, SuccessExtra

from .models import Event
from .schemas import EventCreate, EventUpdate, EventInDB
from .controllers import event_controller

router = APIRouter()


@router.get("/list", summary="Просмотр списка событий")
async def list_events(
    page: int = Query(1, ge=1, description="Номер страницы (начиная с 1)"),
    page_size: int = Query(10, ge=1, le=100, description="Количество на странице (макс. 100)"),
):
    async with SessionLocal() as session:
        events = await event_controller.get_all(session=session, skip=(page - 1) * page_size, limit=page_size)
        total = await event_controller.count(session=session)

    return SuccessExtra(data=events, total=total, page=page, page_size=page_size)



@router.get("/get", summary="Просмотр события")
async def get_event(
    event_id: int = Query(..., description="ID события"),
    session: AsyncSession = Depends(get_session)
):
    result = await event_controller.get(id=event_id, session=session)
    if not result:
        raise HTTPException(status_code=404, detail="Event not found")
    return Success(data=result)


@router.post("/create", summary="Создание события")
async def create_event(
    event_in: EventCreate,
    session: AsyncSession = Depends(get_session)
):
    await event_controller.create(obj_in=event_in, session=session)
    return Success(msg="Создание успешно")


@router.post("/update", summary="Обновление события")
async def update_event(
    event_in: EventUpdate,
):
    event = await event_controller.get(id=event_in.id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    await event_controller.update(id=event_in.id, obj_in=event_in)
    return Success(msg="Обновление успешно")


@router.delete("/delete", summary="Удаление события")
async def delete_event(
    event_id: int = Query(..., description="ID события"),
):
    event = await event_controller.get(id=event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    await event_controller.remove(id=event_id)
    return Success(msg="Удаление успешно")
