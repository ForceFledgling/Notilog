from fastapi import APIRouter

from .menus import router

menus_router = APIRouter()
menus_router.include_router(router, tags=["Модуль меню"])

__all__ = ["menus_router"]
