from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .endpoints import router

from server import database


app = FastAPI()

# Подключаем маршруты
app.include_router(router)

# Монтируем статические файлы
app.mount("/static", StaticFiles(directory="server/static"), name="static")

# Создаем таблицы, если их нет в базе данных
database.init_db()