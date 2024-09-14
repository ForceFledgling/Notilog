from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base
from app.core.exceptions import SettingNotFound
from app.core.init_app import (
    init_menus,
    init_superuser,
    make_middlewares,
    register_exceptions,
    register_routers,
)
from app.settings.config import settings

# Создание асинхронного движка
engine = create_async_engine(settings.DB_URL, echo=True)
# Создание фабрики сессий
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        # Создание таблиц в базе данных
        await conn.run_sync(Base.metadata.create_all)
    await init_superuser()
    await init_menus()
    yield
    # Не требуется явного закрытия для SQLAlchemy engine

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_TITLE,
        description=settings.APP_DESCRIPTION,
        version=settings.VERSION,
        openapi_url="/openapi.json",
        middleware=make_middlewares(),
        lifespan=lifespan,
    )
    register_exceptions(app)
    register_routers(app, prefix="/api")
    return app

app = create_app()
