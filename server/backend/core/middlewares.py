import re
from datetime import datetime
from typing import Optional

from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.routing import APIRoute
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.types import ASGIApp, Receive, Scope, Send

from backend.core.dependency import AuthControl
from backend.modules.users.models import User
from backend.modules.auditlog.models import AuditLog
from backend.core.database import SessionLocal

from .bgtask import BgTasks

class SimpleBaseMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive=receive)

        response = await self.before_request(request) or self.app
        await response(request.scope, request.receive, send)
        await self.after_request(request)

    async def before_request(self, request: Request):
        return self.app

    async def after_request(self, request: Request):
        return None

class BackGroundTaskMiddleware(SimpleBaseMiddleware):
    async def before_request(self, request):
        await BgTasks.init_bg_tasks_obj()

    async def after_request(self, request):
        await BgTasks.execute_tasks()

class HttpAuditLogMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, methods: list, exclude_paths: list):
        super().__init__(app)
        self.methods = methods
        self.exclude_paths = exclude_paths

    async def get_request_log(self, request: Request, response: Response) -> dict:
        """
        Получение данных журнала на основе объектов request и response
        """
        data: dict = {"path": request.url.path, "status": response.status_code, "method": request.method}
        # Информация о маршруте
        app: FastAPI = request.app
        for route in app.routes:
            if (
                isinstance(route, APIRoute)
                and route.path_regex.match(request.url.path)
                and request.method in route.methods
            ):
                data["module"] = ",".join(route.tags)
                data["summary"] = route.summary
        # Получение информации о пользователе
        token = request.headers.get("token")
        user_obj = None
        if token:
            user_obj: User = await AuthControl.is_authed(token)
        data["user_id"] = user_obj.id if user_obj else 0
        data["username"] = user_obj.username if user_obj else ""
        return data

    async def before_request(self, request: Request):
        pass

    async def after_request(self, request: Request, response: Response, process_time: int):
        if request.method in self.methods:  # Метод запроса соответствует конфигурации для записи
            for path in self.exclude_paths:
                if re.search(path, request.url.path, re.I) is not None:
                    return
            data: dict = await self.get_request_log(request=request, response=response)
            data["response_time"] = process_time  # Время ответа
            
            # Создание записи в журнале с использованием SQLAlchemy
            async with SessionLocal() as session:
                async with session.begin():
                    audit_log = AuditLog(**data)
                    session.add(audit_log)
                    await session.commit()

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time: datetime = datetime.now()
        await self.before_request(request)
        response = await call_next(request)
        end_time: datetime = datetime.now()
        process_time = int((end_time.timestamp() - start_time.timestamp()) * 1000)
        await self.after_request(request, response, process_time)
        return response
