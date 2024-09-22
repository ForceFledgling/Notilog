from fastapi import APIRouter

from .endpoints import router

apis_router = APIRouter()
apis_router.include_router(router, tags=["API Модуль"])

__all__ = ["apis_router"]
