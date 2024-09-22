# server/app/controllers/menu.py

from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from backend.core.crud import CRUDBase
from backend.modules.menus.models import Menu
from .schemas import MenuCreate, MenuUpdate
from backend.core.database import get_session  # Импортируйте функцию для получения сессии

class MenuController(CRUDBase[Menu, MenuCreate, MenuUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Menu, session=session)

    async def get_by_menu_path(self, path: str) -> Optional[Menu]:
        async with self.session() as session:
            q = select(Menu).filter_by(path=path)
            result = await session.execute(q)
            return result.scalars().first()

# Получение сессии
session = get_session()  # Предположим, что у вас есть функция для получения сессии
menu_controller = MenuController(session=session)
