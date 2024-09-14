# server/app/controllers/api.py

from fastapi.routing import APIRoute
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.crud import CRUDBase
from app.log import logger
from app.models.admin import Api
from app.schemas.apis import ApiCreate, ApiUpdate
from app.core.database import get_session  # Импортируйте функцию для получения сессии

class ApiController(CRUDBase[Api, ApiCreate, ApiUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Api, session=session)

    async def refresh_api(self):
        from app import app

        # Удалить устаревшие данные API
        all_api_list = []
        for route in app.routes:
            if isinstance(route, APIRoute):
                all_api_list.append((list(route.methods)[0], route.path))
        delete_api = []
        for api in await Api.all():
            if (api.method, api.path) not in all_api_list:
                delete_api.append((api.method, api.path))
        for item in delete_api:
            method, path = item
            logger.debug(f"API Deleted {method} {path}")
            await Api.filter(method=method, path=path).delete()

        for route in app.routes:
            if isinstance(route, APIRoute):
                method = list(route.methods)[0]
                path = route.path
                summary = route.summary
                tags = list(route.tags)[0]
                api_obj = await Api.filter(method=method, path=path).first()
                if api_obj:
                    logger.debug(f"API Updated {method} {path}")
                    await api_obj.update(method=method, path=path, summary=summary, tags=tags)
                else:
                    logger.debug(f"API Created {method} {path}")
                    await Api.create(method=method, path=path, summary=summary, tags=tags)

# Получение сессии
session = get_session()  # Предположим, что у вас есть функция для получения сессии
api_controller = ApiController(session=session)
