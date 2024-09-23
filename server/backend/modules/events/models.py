from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime

from backend.modules.base.models import BaseModel


class Event(BaseModel):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True)                          # Уникальный идентификатор события для его отслеживания.
    host = Column(String(20), index=True)                           # Название или адрес хоста, с которого пришел лог.
    source = Column(String(30), index=True)                         # Сервис или модуль, который сгенерировал лог.
    service = Column(String(30), index=True)                        # Источник лога, указывающий на приложение, службу или процесс.
    environment = Column(String(20), index=True)                    # Окружение, где было сгенерировано событие.
    context = Column(JSON, nullable=True)                           # Дополнительные данные, предоставляющие контекст для события.
    request_id = Column(String(50), index=True, nullable=True)      # Идентификатор HTTP-запроса или другого типа запроса, связанного с логом.
    correlation_id = Column(String(50), index=True, nullable=True)  # Идентификатор для связи нескольких логов в рамках одного бизнес-процесса.
    level = Column(String(20))                                      # Уровень серьезности события. Примеры: DEBUG, INFO, WARNING, ERROR, CRITICAL.
    stack_trace = Column(Text, nullable=True)                       # Поле для хранения трассировки стека в случае ошибки.
    message = Column(String(255))                                   # Описание самого события.
    timestamp = Column(DateTime, default=datetime.utcnow)           # Время, когда произошло событие, с значением по умолчанию - текущее время.
