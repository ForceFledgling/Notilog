from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from .models import Event, SessionLocal, init_db
from .config import settings
from .notifications import send_notification
from pydantic import BaseModel
import celery

app = FastAPI()

# Инициализация базы данных при запуске сервера
@app.on_event("startup")
def startup():
    init_db()

# Dependency для работы с сессиями БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Схема события
class EventCreate(BaseModel):
    title: str
    description: str
    level: str

@app.post("/events/")
def create_event(event: EventCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    db_event = Event(title=event.title, description=event.description, level=event.level)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    
    # Запуск задачи по отправке уведомления
    background_tasks.add_task(send_notification, db_event)
    
    return db_event
