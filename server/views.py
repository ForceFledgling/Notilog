from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import desc

from .models import Event
from .database import init_db, get_db

app = FastAPI()

# Инициализация базы данных
init_db()

# Настройка статики
app.mount("/static", StaticFiles(directory="server/static"), name="static")

# Настройка шаблонов
templates = Jinja2Templates(directory="server/templates")

@app.get("/", response_class=HTMLResponse)
async def read_events(request: Request, db: Session = Depends(get_db)):
    events = db.query(Event).order_by(desc(Event.timestamp)).all()
    return templates.TemplateResponse("index.html", {"request": request, "events": events})
