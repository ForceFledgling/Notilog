from fastapi import APIRouter

from .roles import router

roles_router = APIRouter()
roles_router.include_router(router, tags=["Модуль ролей"])

__all__ = ["roles_router"]
