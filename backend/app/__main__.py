import uvicorn

from app.core.config import settings


uvicorn.run(
    'app.main:app',
    host="127.0.0.1",
    port=8000,
    reload=True,
)