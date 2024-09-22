from fastapi.routing import APIRoute
from sqlalchemy.future import select
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.crud import CRUDBase
from backend.core.database import get_session
from backend.core.log import logger

from .models import Api
from .schemas import ApiCreate, ApiUpdate


class ApiController(CRUDBase[Api, ApiCreate, ApiUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Api, session=session)

    async def refresh_api(self):
        from backend import app
        # Получение списка всех существующих API
        all_api_list = []
        for route in app.routes:
            if isinstance(route, APIRoute):
                all_api_list.append((list(route.methods)[0], route.path))

        # Получение всех API из базы данных
        async with self.session() as session:
            result = await session.execute(select(Api))
            api_objs = result.scalars().all()

            # Поиск API, которые нужно удалить
            delete_api = []
            for api in api_objs:
                if (api.method, api.path) not in all_api_list:
                    delete_api.append((api.method, api.path))

            # Удаление устаревших API
            for method, path in delete_api:
                logger.debug(f"API Deleted {method} {path}")
                await session.execute(delete(Api).where(Api.method == method, Api.path == path))
                await session.commit()

            # Обновление или создание новых API
            for route in app.routes:
                if isinstance(route, APIRoute):
                    method = list(route.methods)[0]
                    path = route.path
                    summary = route.summary
                    tags = list(route.tags)[0]

                    api_obj = await session.execute(select(Api).where(Api.method == method, Api.path == path))
                    api_obj = api_obj.scalar()

                    if api_obj:
                        logger.debug(f"API Updated {method} {path}")
                        api_obj.summary = summary
                        api_obj.tags = tags
                        session.add(api_obj)
                    else:
                        logger.debug(f"API Created {method} {path}")
                        new_api = Api(method=method, path=path, summary=summary, tags=tags)
                        session.add(new_api)

            await session.commit()


session = get_session()
api_controller = ApiController(session=session)
