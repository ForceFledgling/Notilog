from fastapi import APIRouter

from .endpoints import router


users_router = APIRouter()
users_router.include_router(router, tags=["Модуль пользователей"])

__all__ = ["users_router"]
