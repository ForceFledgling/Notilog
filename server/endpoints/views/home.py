from fastapi import APIRouter, FastAPI, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import desc

from server.models import Event
from server.database import init_db, get_db


router = APIRouter()

# Настройка шаблонов
templates = Jinja2Templates(directory="server/templates")

@router.get("/", response_class=HTMLResponse)
async def read_events(request: Request, db: Session = Depends(get_db)):
    events = db.query(Event).order_by(desc(Event.timestamp)).all()
    return templates.TemplateResponse("index.html", {"request": request, "events": events})
