from fastapi import APIRouter, Query
from tortoise.expressions import Q

from app.controllers.api import api_controller
from app.schemas import Success, SuccessExtra
from app.schemas.apis import *

router = APIRouter()


@router.get("/list", summary="Просмотр списка API")
async def list_api(
    page: int = Query(1, description="Номер страницы"),
    page_size: int = Query(10, description="Количество на странице"),
    path: str = Query(None, description="Путь API"),
    summary: str = Query(None, description="Описание API"),
    tags: str = Query(None, description="Теги API"),
):
    q = Q()
    if path:
        q &= Q(path__contains=path)
    if summary:
        q &= Q(summary__contains=summary)
    if tags:
        q &= Q(tags__contains=tags)
    total, api_objs = await api_controller.list(page=page, page_size=page_size, search=q, order=["tags", "id"])
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
