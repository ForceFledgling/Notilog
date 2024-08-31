from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy import desc

from .models import init_db, Event
from .database import get_db  # Импортируем функцию get_db

app = FastAPI()

# Инициализируем базу данных
init_db()

# Настройка статики
app.mount("/static", StaticFiles(directory="server/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_events(db: Session = Depends(get_db)):
    events = db.query(Event).order_by(desc(Event.timestamp)).all()
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>NotiLog</title>
        <link rel="stylesheet" href="/static/css/styles.css">
    </head>
    <body>
        <h1>События</h1>
        <table>
            <thead>
                <tr>
                    <th>Приложение</th>
                    <th>Время события</th>
                    <th>Уровень события</th>
                    <th>Сообщение</th>
                </tr>
            </thead>
            <tbody>
    """
    for event in events:
        html_content += f"""
                <tr>
                    <td>{event.title}</td>
                    <td>{event.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</td>
                    <td>{event.level}</td>
                    <td>{event.description}</td>
                </tr>
        """
    
    html_content += """
            </tbody>
        </table>
        <script src="/static/js/script.js"></script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)
