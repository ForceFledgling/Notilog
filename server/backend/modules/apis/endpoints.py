from fastapi import APIRouter, Query

from sqlalchemy.future import select
from sqlalchemy import or_, and_
from sqlalchemy.sql import func

from backend.modules.base.schemas import Success, SuccessExtra
from .schemas import *
from backend.core.database import SessionLocal

from .controllers import api_controller


router = APIRouter()


@router.get("/list", summary="Просмотр списка API")
async def list_api(
    page: int = Query(1, description="Номер страницы"),
    page_size: int = Query(10, description="Количество на странице"),
    path: str = Query(None, description="Путь API"),
    summary: str = Query(None, description="Описание API"),
    tags: str = Query(None, description="Теги API"),
):
    async with SessionLocal() as session:
        query = select(api_controller.model)
        
        # Добавляем условия поиска
        if path:
            query = query.filter(api_controller.model.path.contains(path))
        if summary:
            query = query.filter(api_controller.model.summary.contains(summary))
        if tags:
            query = query.filter(api_controller.model.tags.contains(tags))
        
        # Выполняем запрос и получаем результат с пагинацией
        result = await session.execute(query.order_by(api_controller.model.tags, api_controller.model.id).offset((page - 1) * page_size).limit(page_size))
        api_objs = result.scalars().all()

        # Подсчитываем общее количество элементов
        count_query = select(func.count()).select_from(api_controller.model)
        total_result = await session.execute(count_query)
        total = total_result.scalar()

        data = [await obj.to_dict() for obj in api_objs]
        return SuccessExtra(data=data, total=total, page=page, page_size=page_size)


@router.get("/get", summary="Просмотр API")
async def get_api(
    id: int = Query(..., description="ID API"),
):
    api_obj = await api_controller.get(id=id)
    data = await api_obj.to_dict()
    return Success(data=data)


@router.post("/create", summary="Создание API")
async def create_api(
    api_in: ApiCreate,
):
    await api_controller.create(obj_in=api_in)
    return Success(msg="Успешно создано")


@router.post("/update", summary="Обновление API")
async def update_api(
    api_in: ApiUpdate,
):
    await api_controller.update(id=api_in.id, obj_in=api_in)
    return Success(msg="Успешно обновлено")


@router.delete("/delete", summary="Удаление API")
async def delete_api(
    api_id: int = Query(..., description="ID API"),
):
    await api_controller.remove(id=api_id)
    return Success(msg="Успешно удалено")


@router.post("/refresh", summary="Обновление списка API")
async def refresh_api():
    await api_controller.refresh_api()
    return Success(msg="OK")
