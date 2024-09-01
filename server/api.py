from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from pydantic import BaseModel
import celery

from .models import Event
from .database import get_db
from .config import settings
from .notifications import send_notification

from server.views import app
from server.views import app as views_app


app = FastAPI()

# Подключаем маршруты из views.py
app.include_router(views_app.router)

# Монтируем статические файлы
app.mount("/static", StaticFiles(directory="server/static"), name="static")


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


@app.post("/events/")
def create_event(event: EventCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)) -> Event:
    db_event = Event(title=event.title, description=event.description, level=event.level)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    
    # Запуск задачи по отправке уведомления
    background_tasks.add_task(send_notification, db_event)
    
    return db_event
