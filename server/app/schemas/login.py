from datetime import datetime

from pydantic import BaseModel, Field


class CredentialsSchema(BaseModel):
    username: str = Field(..., description="Имя пользователя", example="admin")  # Описание: Имя пользователя
    password: str = Field(..., description="Пароль", example="123456")  # Описание: Пароль


class JWTOut(BaseModel):
    access_token: str  # Токен доступа
    username: str  # Имя пользователя


class JWTPayload(BaseModel):
    user_id: int  # Идентификатор пользователя
    username: str  # Имя пользователя
    is_superuser: bool  # Флаг суперпользователя
    exp: datetime  # Время истечения токена
