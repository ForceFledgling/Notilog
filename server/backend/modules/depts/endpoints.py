from fastapi import APIRouter, Query

from backend.schemas import Success
from backend.schemas.depts import *

from .controllers import dept_controller


router = APIRouter()


@router.get("/list", summary="Просмотреть список отделов")
async def list_dept(
    name: str = Query(None, description="Название отдела"),
):
    dept_tree = await dept_controller.get_dept_tree(name)
    return Success(data=dept_tree)


@router.get("/get", summary="Просмотреть отдел")
async def get_dept(
    id: int = Query(..., description="ID отдела"),
):
    dept_obj = await dept_controller.get(id=id)
    data = await dept_obj.to_dict()
    return Success(data=data)


@router.post("/create", summary="Создать отдел")
async def create_dept(
    dept_in: DeptCreate,
):
    await dept_controller.create_dept(obj_in=dept_in)
    return Success(msg="Успешно создано")


@router.post("/update", summary="Обновить отдел")
async def update_dept(
    dept_in: DeptUpdate,
):
    await dept_controller.update_dept(obj_in=dept_in)
    return Success(msg="Успешно обновлено")


@router.delete("/delete", summary="Удалить отдел")
async def delete_dept(
    dept_id: int = Query(..., description="ID отдела"),
):
    await dept_controller.delete_dept(dept_id=dept_id)
    return Success(msg="Успешно удалено")
