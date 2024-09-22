from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.crud import CRUDBase
from backend.core.database import get_session
from backend.modules.apis.models import Api
from backend.modules.menus.models import Menu

from .models import Role
from .schemas import RoleCreate, RoleUpdate


class RoleController(CRUDBase[Role, RoleCreate, RoleUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Role, session=session)

    async def is_exist(self, name: str) -> bool:
        return await self.model.filter(name=name).exists()

    async def update_roles(self, role: Role, menu_ids: List[int], api_infos: List[dict]) -> None:
        await role.menus.clear()
        for menu_id in menu_ids:
            menu_obj = await Menu.filter(id=menu_id).first()
            await role.menus.add(menu_obj)

        await role.apis.clear()
        for item in api_infos:
            api_obj = await Api.filter(path=item.get("path"), method=item.get("method")).first()
            await role.apis.add(api_obj)


session = get_session()
role_controller = RoleController(session=session)
