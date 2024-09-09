from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class BaseRole(BaseModel):
    id: int
    name: str
    desc: str = ""  # Описание роли
    users: Optional[list] = []  # Список пользователей, связанных с ролью
    menus: Optional[list] = []  # Список меню, связанных с ролью
    apis: Optional[list] = []  # Список API, связанных с ролью
    created_at: Optional[datetime]  # Дата создания роли
    updated_at: Optional[datetime]  # Дата последнего обновления роли


class RoleCreate(BaseModel):
    name: str = Field(example="Администратор")  # Название роли, пример "Администратор"
    desc: str = Field("", example="Роль администратора")  # Описание роли, пример "Роль администратора"


class RoleUpdate(BaseModel):
    id: int = Field(example=1)  # Идентификатор роли, пример 1
    name: str = Field(example="Администратор")  # Название роли, пример "Администратор"
    desc: str = Field("", example="Роль администратора")  # Описание роли, пример "Роль администратора"


class RoleUpdateMenusApis(BaseModel):
    id: int  # Идентификатор роли
    menu_ids: list[int] = []  # Список идентификаторов меню
    api_infos: list[dict] = []  # Список информации об API
