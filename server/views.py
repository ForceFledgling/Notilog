# server/views.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

# Инициализация приложения и шаблонизатора
app = FastAPI()
templates = Jinja2Templates(directory="server/templates")

# Маршрут для обработки статических файлов
app.mount("/static", StaticFiles(directory="server/static"), name="static")

# Маршрут для главной страницы
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    context = {"message": "Hello, FastAPI with Jinja2!"}
    return templates.TemplateResponse("index.html", {"request": request, **context})
