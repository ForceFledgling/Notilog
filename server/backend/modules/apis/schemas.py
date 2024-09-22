from pydantic import BaseModel, Field

from backend.core.enums import MethodType


class BaseApi(BaseModel):
    path: str = Field(..., description="Путь API", example="/api/v1/user/list")
    summary: str = Field("", description="Описание API", example="Просмотр списка пользователей")
    method: MethodType = Field(..., description="Метод API", example="GET")
    tags: str = Field(..., description="Теги API", example="User")

class ApiCreate(BaseApi):
    ...  # Пустое тело класса для создания API

class ApiUpdate(BaseApi):
    id: int  # Идентификатор для обновления существующего API
