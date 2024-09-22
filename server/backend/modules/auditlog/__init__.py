from fastapi import APIRouter

from .endpoints import router


auditlog_router = APIRouter()
auditlog_router.include_router(router, tags=["Модуль аудита журналов"])

__all__ = ["auditlog_router"]
