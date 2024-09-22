from fastapi import APIRouter

from .endpoints import router

roles_router = APIRouter()
roles_router.include_router(router, tags=["Модуль ролей"])

__all__ = ["roles_router"]
