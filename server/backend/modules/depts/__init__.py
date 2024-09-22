from fastapi import APIRouter

from .endpoints import router

depts_router = APIRouter()
depts_router.include_router(router, tags=["Модуль подразделений"])

__all__ = ["depts_router"]
