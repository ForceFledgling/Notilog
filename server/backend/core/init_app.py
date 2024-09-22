from fastapi import FastAPI
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

from backend.api import api_router
from backend.modules.users.controllers import UserCreate, user_controller
from backend.core.exceptions import (
    DoesNotExist,
    DoesNotExistHandle,
    HTTPException,
    HttpExcHandle,
    IntegrityError,
    IntegrityHandle,
    RequestValidationError,
    RequestValidationHandle,
    ResponseValidationError,
    ResponseValidationHandle,
)
from backend.models.admin import Menu
from backend.schemas.menus import MenuType
from backend.settings.config import settings

from .middlewares import BackGroundTaskMiddleware, HttpAuditLogMiddleware

from sqlalchemy.future import select
from backend.core.database import SessionLocal
from backend.models import User

def make_middlewares():
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ORIGINS,
            allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
            allow_methods=settings.CORS_ALLOW_METHODS,
            allow_headers=settings.CORS_ALLOW_HEADERS,
        ),
        Middleware(BackGroundTaskMiddleware),
        Middleware(
            HttpAuditLogMiddleware,
            methods=["GET", "POST", "PUT", "DELETE"],
            exclude_paths=[
                "/docs",
                "/openapi.json",
            ],
        ),
    ]
    return middleware


def register_exceptions(app: FastAPI):
    app.add_exception_handler(DoesNotExist, DoesNotExistHandle)
    app.add_exception_handler(HTTPException, HttpExcHandle)
    app.add_exception_handler(IntegrityError, IntegrityHandle)
    app.add_exception_handler(RequestValidationError, RequestValidationHandle)
    app.add_exception_handler(ResponseValidationError, ResponseValidationHandle)


def register_routers(app: FastAPI, prefix: str = "/api"):
    app.include_router(api_router, prefix=prefix)


async def init_superuser():
    async with SessionLocal() as session:
        async with session.begin():
            result = await session.execute(select(User).filter(User.username == 'admin'))
            user = result.scalars().first()
            if not user:
                # Создание пользователя, если его нет
                await user_controller.create_user(
                    UserCreate(
                        username="admin",
                        email="admin@admin.com",
                        password="123456",
                        is_active=True,
                        is_superuser=True,
                    )
                )


async def init_menus():
    async with SessionLocal() as session:
        async with session.begin():
            # Проверьте наличие записей в таблице Menu
            result = await session.execute(select(Menu))
            menus = result.scalars().all()
            
            if not menus:
                parent_menu = Menu(
                    menu_type=MenuType.CATALOG,
                    name="Системное управление",
                    path="/system",
                    order=1,
                    parent_id=0,
                    icon="carbon:gui-management",
                    is_hidden=False,
                    component="Layout",
                    keepalive=False,
                    redirect="/system/user",
                )
                session.add(parent_menu)
                await session.flush()  # Убедитесь, что parent_menu имеет id после flush
                
                children_menu = [
                    Menu(
                        menu_type=MenuType.MENU,
                        name="Управление пользователями",
                        path="user",
                        order=1,
                        parent_id=parent_menu.id,
                        icon="material-symbols:person-outline-rounded",
                        is_hidden=False,
                        component="/system/user",
                        keepalive=False,
                    ),
                    Menu(
                        menu_type=MenuType.MENU,
                        name="Управление ролями",
                        path="role",
                        order=2,
                        parent_id=parent_menu.id,
                        icon="carbon:user-role",
                        is_hidden=False,
                        component="/system/role",
                        keepalive=False,
                    ),
                    Menu(
                        menu_type=MenuType.MENU,
                        name="Управление меню",
                        path="menu",
                        order=3,
                        parent_id=parent_menu.id,
                        icon="material-symbols:list-alt-outline",
                        is_hidden=False,
                        component="/system/menu",
                        keepalive=False,
                    ),
                    Menu(
                        menu_type=MenuType.MENU,
                        name="Управление API",
                        path="api",
                        order=4,
                        parent_id=parent_menu.id,
                        icon="ant-design:api-outlined",
                        is_hidden=False,
                        component="/system/api",
                        keepalive=False,
                    ),
                    Menu(
                        menu_type=MenuType.MENU,
                        name="Управление отделами",
                        path="dept",
                        order=5,
                        parent_id=parent_menu.id,
                        icon="mingcute:department-line",
                        is_hidden=False,
                        component="/system/dept",
                        keepalive=False,
                    ),
                    Menu(
                        menu_type=MenuType.MENU,
                        name="Аудит журналов",
                        path="auditlog",
                        order=6,
                        parent_id=parent_menu.id,
                        icon="ph:clipboard-text-bold",
                        is_hidden=False,
                        component="/system/auditlog",
                        keepalive=False,
                    ),
                ]
                session.add_all(children_menu)

                # Добавление верхнего уровня меню
                top_menu = Menu(
                    menu_type=MenuType.MENU,
                    name="Верхнее меню",
                    path="/top-menu",
                    order=2,
                    parent_id=0,
                    icon="material-symbols:featured-play-list-outline",
                    is_hidden=False,
                    component="/top-menu",
                    keepalive=False,
                    redirect="",
                )
                session.add(top_menu)

                await session.commit()
