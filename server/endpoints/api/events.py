from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel

from server.models import Event
from server.database import get_db
from server.notifications import send_notification


router = APIRouter()


class EventCreate(BaseModel):
    """
    Модель для создания нового события.

    Attributes:
        title: Заголовок события. Описывает краткое название или тему события.
        description: Описание события. Содержит подробное описание того, что произошло.
        level: Уровень события. Определяет степень важности или приоритета события (например, 'info', 'warning', 'error').
    """
    title: str
    description: str
    level: str


@router.post("/events/")
def create_event(event: EventCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    Создает новое событие и запускает фоновую задачу для отправки уведомления.

    Этот метод обрабатывает POST-запросы для создания нового события в базе данных. 
    Входные данные принимаются в виде модели `EventCreate`, которая содержит заголовок, описание и уровень события.

    После создания события:
        1. Оно сохраняется в базе данных.
        2. Запускается фоновая задача `send_notification` для отправки уведомления о новом событии.

    Attributes:
        event (EventCreate): Данные нового события.
        background_tasks (BackgroundTasks): Объект для управления фоновыми задачами.
        db (Session): Сессия базы данных, автоматически предоставляемая через зависимость `get_db`.

    Returns:
        Event: Объект события, который был создан и сохранен в базе данных.

    Примечание:
        Фоновая задача `send_notification` будет выполнена асинхронно после того, как основной запрос завершится.
    """
    db_event = Event(title=event.title, description=event.description, level=event.level)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    
    # Запуск задачи по отправке уведомления
    background_tasks.add_task(send_notification, db_event)
    
    return db_event
