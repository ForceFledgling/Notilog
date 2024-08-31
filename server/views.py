from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from .models import SessionLocal, init_db, Event

app = FastAPI()

# Инициализируем базу данных
init_db()

# Настройка статики
app.mount("/static", StaticFiles(directory="server/static"), name="static")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def read_events(db: Session = Depends(get_db)):
    events = db.query(Event).all()
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Events</title>
        <link rel="stylesheet" href="/static/css/styles.css">
    </head>
    <body>
        <h1>Events</h1>
        <table>
            <thead>
                <tr>
                    <th>Title</th>
                    <th>Timestamp</th>
                    <th>Level</th>
                    <th>Description</th>
                </tr>
            </thead>
            <tbody>
    """
    + "".join(f"""
                <tr>
                    <td>{event.title}</td>
                    <td>{event.timestamp.strftime('%Y-%m-%d %H:%M:%S')}</td>
                    <td>{event.level}</td>
                    <td>{event.description}</td>
                </tr>
    """ for event in events) +
    """
            </tbody>
        </table>
        <script src="/static/js/script.js"></script>
    </body>
    </html>
    """
