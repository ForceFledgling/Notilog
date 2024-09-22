# backend/core/dependency.py

from typing import Optional

import jwt
from fastapi import Depends, Header, HTTPException, Request

from backend.core.ctx import CTX_USER_ID
from backend.settings import settings
from backend.core.database import SessionLocal

from sqlalchemy.future import select


class AuthControl:
    @classmethod
    async def is_authed(cls, token: str = Header(..., description="Проверка токена")) -> Optional["User"]:
        from backend.modules.users.models import User  # Перенос импорта внутрь функции
        try:
            async with SessionLocal() as session:
                if token == "dev":
                    stmt = select(User)
                    result = await session.execute(stmt)
                    user = result.scalars().first()
                    user_id = user.id if user else None
                else:
                    decode_data = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
                    user_id = decode_data.get("user_id")

                if user_id is None:
                    raise HTTPException(status_code=401, detail="Ошибка аутентификации")

                stmt = select(User).where(User.id == user_id)
                result = await session.execute(stmt)
                user = result.scalars().first()
                
                if not user:
                    raise HTTPException(status_code=401, detail="Ошибка аутентификации")

                CTX_USER_ID.set(int(user_id))
                return user

        except jwt.DecodeError:
            raise HTTPException(status_code=401, detail="Недействительный токен")
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Срок действия токена истек")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"{repr(e)}")


class PermissionControl:
    @classmethod
    async def has_permission(cls, request: Request, current_user: "User" = Depends(AuthControl.is_authed)) -> None:
        from backend.models.admin import Role  # Перенос импорта внутрь функции
        if current_user.is_superuser:
            return
        method = request.method
        path = request.url.path
        roles: list[Role] = await current_user.roles
        if not roles:
            raise HTTPException(status_code=403, detail="The user is not bound to a role")
        apis = [await role.apis for role in roles]
        permission_apis = list(set((api.method, api.path) for api in sum(apis, [])))
        if (method, path) not in permission_apis:
            raise HTTPException(status_code=403, detail=f"Permission denied method:{method} path:{path}")


DependAuth = Depends(AuthControl.is_authed)
DependPermisson = Depends(PermissionControl.has_permission)
