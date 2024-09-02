from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .endpoints import router


app = FastAPI()

# Подключаем маршруты
app.include_router(router)

# Монтируем статические файлы
app.mount("/static", StaticFiles(directory="server/static"), name="static")
