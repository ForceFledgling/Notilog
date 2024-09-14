from fastapi import APIRouter, Query, Depends
from app.models.admin import AuditLog
from app.schemas import SuccessExtra
from app.core.database import get_session, SessionLocal
from app.core.dependency import DependPermisson

from sqlalchemy import func, select, and_, or_, between
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()

@router.get('/list', summary="Просмотр логов операций", dependencies=[DependPermisson])
async def get_audit_log_list(
    page: int = Query(1, description="Номер страницы"),
    page_size: int = Query(10, description="Количество на странице"),
    username: str = Query("", description="Имя оператора"),
    module: str = Query("", description="Модуль функции"),
    summary: str = Query("", description="Описание интерфейса"),
    start_time: str = Query("", description="Начальное время"),
    end_time: str = Query("", description="Конечное время"),
):
    async with AsyncSession() as session:
        filters = []
        if username:
            filters.append(AuditLog.username.ilike(f'%{username}%'))
        if module:
            filters.append(AuditLog.module.ilike(f'%{module}%'))
        if summary:
            filters.append(AuditLog.summary.ilike(f'%{summary}%'))
        if start_time and end_time:
            filters.append(AuditLog.created_at.between(start_time, end_time))
        elif start_time:
            filters.append(AuditLog.created_at >= start_time)
        elif end_time:
            filters.append(AuditLog.created_at <= end_time)
        
        # Основной запрос для получения данных
        stmt = select(AuditLog).where(and_(*filters)).offset((page - 1) * page_size).limit(page_size).order_by(AuditLog.created_at.desc())
        result = await session.execute(stmt)
        audit_log_objs = result.scalars().all()
        
        # Запрос для подсчета общего количества записей
        count_stmt = select(func.count()).select_from(AuditLog).where(and_(*filters))
        count_result = await session.execute(count_stmt)
        total = count_result.scalar()

        data = [await audit_log.to_dict() for audit_log in audit_log_objs]
        return SuccessExtra(data=data, total=total, page=page, page_size=page_size)
