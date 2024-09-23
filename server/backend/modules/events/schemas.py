from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class EventBase(BaseModel):
    """
    Базовая схема, которая используется для создания и обновления события.
    Все поля являются необязательными (Optional),
    что позволяет использовать эту схему в других контекстах (например, для обновлений или чтения данных).
    """
    host: Optional[str] = None                           # Название или адрес хоста
    source: Optional[str] = None                         # Сервис или модуль, который сгенерировал лог
    service: Optional[str] = None                        # Источник лога (приложение, служба или процесс)
    environment: Optional[str] = None                    # Окружение (production, staging и т.д.)
    context: Optional[dict] = None                       # Дополнительные данные (в формате JSON)
    request_id: Optional[str] = None                     # Идентификатор запроса
    correlation_id: Optional[str] = None                 # Идентификатор для связи логов в рамках процесса
    level: Optional[str] = None                          # Уровень серьезности (DEBUG, INFO и т.д.)
    stack_trace: Optional[str] = None                    # Трассировка стека для ошибок
    message: Optional[str] = None                        # Описание события

    class Config:
        orm_mode = True


class EventCreate(EventBase):
    """
    Cхема для создания нового события.
    В ней обязательны поля host, source, service, environment, level и message,
    поскольку они необходимы для создания события.
    """
    host: str
    source: str
    service: str
    environment: str
    level: str
    message: str


class EventUpdate(EventBase):
    """
    Cхема для обновления события.
    Наследует от EventBase, и она позволяет частично обновлять событие.
    """
    pass


class EventInDB(EventBase):
    """
    Схема, представляющая данные, полученные из БД.
    Добавлены поля id и timestamp для полной модели события, включая идентификатор и метку времени.
    """
    id: int
    timestamp: datetime                                  # Время создания события

    class Config:
        orm_mode = True
