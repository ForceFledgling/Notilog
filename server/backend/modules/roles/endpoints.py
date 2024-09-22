import logging

from fastapi import APIRouter, Query
from fastapi.exceptions import HTTPException
from tortoise.expressions import Q

from .controllers import role_controller
from backend.modules.base.schemas import Success, SuccessExtra
from .schemas import *

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/list", summary="Просмотр списка ролей")
async def list_role(
    page: int = Query(1, description="Номер страницы"),
    page_size: int = Query(10, description="Количество элементов на странице"),
    role_name: str = Query("", description="Название роли для поиска"),
):
    filters = {}
    if role_name:
        filters["name__contains"] = role_name
    
    total, role_objs = await role_controller.list(page=page, page_size=page_size, **filters)
    data = [await obj.to_dict() for obj in role_objs]
    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)



@router.get("/get", summary="Просмотр роли")
async def get_role(
    role_id: int = Query(..., description="ID роли"),
):
    role_obj = await role_controller.get(id=role_id)
    return Success(data=await role_obj.to_dict())


@router.post("/create", summary="Создание роли")
async def create_role(role_in: RoleCreate):
    if await role_controller.is_exist(name=role_in.name):
        raise HTTPException(
            status_code=400,
            detail="Роль с таким именем уже существует в системе.",
        )
    await role_controller.create(obj_in=role_in)
    return Success(msg="Успешно создано")


@router.post("/update", summary="Обновление роли")
async def update_role(role_in: RoleUpdate):
    await role_controller.update(id=role_in.id, obj_in=role_in)
    return Success(msg="Успешно обновлено")


@router.delete("/delete", summary="Удаление роли")
async def delete_role(
    role_id: int = Query(..., description="ID роли"),
):
    await role_controller.remove(id=role_id)
    return Success(msg="Успешно удалено")


@router.get("/authorized", summary="Просмотр прав роли")
async def get_role_authorized(id: int = Query(..., description="ID роли")):
    role_obj = await role_controller.get(id=id)
    data = await role_obj.to_dict(m2m=True)
    return Success(data=data)


@router.post("/authorized", summary="Обновление прав роли")
async def update_role_authorized(role_in: RoleUpdateMenusApis):
    role_obj = await role_controller.get(id=role_in.id)
    await role_controller.update_roles(role=role_obj, menu_ids=role_in.menu_ids, api_infos=role_in.api_infos)
    return Success(msg="Успешно обновлено")
