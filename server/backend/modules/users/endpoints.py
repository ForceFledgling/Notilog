from fastapi import APIRouter, Body, Query

from backend.modules.base.schemas import Fail, Success, SuccessExtra
from backend.modules.depts.controllers import dept_controller

from .controllers import user_controller
from .schemas import *


router = APIRouter()


@router.get("/list", summary="Просмотр списка пользователей")
async def list_user(
    page: int = Query(1, description="Номер страницы"),
    page_size: int = Query(10, description="Количество на странице"),
    username: str = Query("", description="Имя пользователя для поиска"),
    email: str = Query("", description="Адрес электронной почты"),
    dept_id: int = Query(None, description="ID отдела"),
):
    filters = {}
    if username:
        filters["username__contains"] = username
    if email:
        filters["email__contains"] = email
    if dept_id is not None:
        filters["dept_id"] = dept_id

    total, user_objs = await user_controller.list(page=page, page_size=page_size, **filters)
    data = [await obj.to_dict(exclude_fields=["password"]) for obj in user_objs]
    for item in data:
        dept_id = item.pop("dept_id", None)
        item["dept"] = await (await dept_controller.get(id=dept_id)).to_dict() if dept_id else {}

    return SuccessExtra(data=data, total=total, page=page, page_size=page_size)


@router.get("/get", summary="Просмотр пользователя")
async def get_user(
    user_id: int = Query(..., description="ID пользователя"),
):
    user_obj = await user_controller.get(id=user_id)
    user_dict = await user_obj.to_dict(exclude_fields=["password"])
    return Success(data=user_dict)


@router.post("/create", summary="Создание пользователя")
async def create_user(
    user_in: UserCreate,
):
    user = await user_controller.get_by_email(user_in.email)
    if user:
        return Fail(code=400, msg="Пользователь с этим адресом электронной почты уже существует.")
    new_user = await user_controller.create_user(obj_in=user_in)
    await user_controller.update_roles(new_user, user_in.role_ids)
    return Success(msg="Успешно создано")


@router.post("/update", summary="Обновление пользователя")
async def update_user(
    user_in: UserUpdate,
):
    user = await user_controller.update(id=user_in.id, obj_in=user_in)
    await user_controller.update_roles(user, user_in.role_ids)
    return Success(msg="Успешно обновлено")


@router.delete("/delete", summary="Удаление пользователя")
async def delete_user(
    user_id: int = Query(..., description="ID пользователя"),
):
    await user_controller.remove(id=user_id)
    return Success(msg="Успешно удалено")


@router.post("/reset_password", summary="Сброс пароля")
async def reset_password(user_id: int = Body(..., description="ID пользователя")):
    await user_controller.reset_password(user_id)
    return Success(msg="Пароль сброшен на 123456")
