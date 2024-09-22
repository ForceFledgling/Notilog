import logging

from fastapi import APIRouter, Query

from backend.modules.base.schemas import Fail, Success, SuccessExtra
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from backend.modules.menus.models import Menu
from fastapi import Depends, Query

from backend.core.database import get_session, SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)

router = APIRouter()


# TODO доделать эндпоинты, добавить модели, схемы и перенести все в отдельный модуль

@router.get("/get", summary="Просмотр события")
async def get_event(
):
    result = {
        "id": "event-12345",                    # Уникальный идентификатор события для его отслеживания. Пример: event-12345
        "host": "127.0.0.1",                    # Имя или IP-адрес сервера, на котором произошло событие. Пример: server-001, 192.168.1.10
        "source": "UFOVPN",                     # Сервис или модуль, который сгенерировал лог. Пример: authentication, payment_gateway
        "service": "wireguard",                 # Источник лога, указывающий на приложение, службу или процесс. Пример: auth_service, database, nginx
        "environment": "production",            # Окружение, где было сгенерировано событие. Пример: production, staging, development
        "context": {},                          # Дополнительные данные, предоставляющие контекст для события. Пример: {"module": "user_auth", "function": "login"}
        "request_id": "req-98765",              # Идентификатор HTTP-запроса или другого типа запроса, связанного с логом. Пример: req-98765
        "correlation_id": "corr-123abc",        # Идентификатор для связи нескольких логов в рамках одного бизнес-процесса. Пример: corr-123abc
        "level": "DEBUG",                       # Уровень серьезности события. Примеры: DEBUG, INFO, WARNING, ERROR, CRITICAL
        "stack_trace": "",                      # Поле для хранения трассировки стека в случае ошибки. Пример: Данные стека вызовов Python или другого языка программирования.
        "message": "Service failed!",           # Описание самого события. Пример: "User admin successfully logged in"
        "timestamp": "20.09.2024 23:26:05",     # Время, когда произошло событие. Пример: 2024-09-20T14:22:35.123Z. Формат: ISO 8601 (UTC) или другой общепринятый формат времени (ВЫБРАТЬ!!!).
    }
    return Success(data=result)


@router.post("/create", summary="Создание события")
async def create_event(
):
    return Success(msg="Создание успешно")
