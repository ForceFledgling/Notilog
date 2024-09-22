from datetime import datetime
from typing import List, Optional

from fastapi.exceptions import HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.crud import CRUDBase
from .models import User
from backend.modules.login.schemas import CredentialsSchema
from .schemas import UserCreate, UserUpdate
from backend.utils.password import get_password_hash, verify_password
from backend.core.database import SessionLocal

from backend.modules.roles.controllers import role_controller


class UserController(CRUDBase[User, UserCreate, UserUpdate]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=User, session=session)

    async def get_by_email(self, email: str) -> Optional[User]:
        async with self.session() as session:
            result = await session.execute(select(self.model).filter_by(email=email))
            return result.scalars().first()

    async def get_by_username(self, username: str) -> Optional[User]:
        async with self.session() as session:
            result = await session.execute(select(self.model).filter_by(username=username))
            return result.scalars().first()

    async def create_user(self, obj_in: UserCreate) -> User:
        obj_in.password = get_password_hash(password=obj_in.password)
        obj = await self.create(obj_in)
        return obj

    async def update_last_login(self, id: int) -> None:
        async with self.session() as session:
            user = await session.get(self.model, id)
            if user:
                user.last_login = datetime.now()
                session.add(user)
                await session.commit()

    async def authenticate(self, credentials: CredentialsSchema) -> Optional["User"]:
        async with self.session() as session:
            result = await session.execute(select(self.model).filter_by(username=credentials.username))
            print('result', result)
            user = result.scalars().first()
            print('user', user)
            if not user:
                raise HTTPException(status_code=400, detail="Неверные имя пользователя или пароль")
            verified = verify_password(credentials.password, user.password)
            if not verified:
                raise HTTPException(status_code=400, detail="Неверный пароль!")
            if not user.is_active:
                raise HTTPException(status_code=400, detail="Пользователь отключен")
            return user

    async def update_roles(self, user: User, role_ids: List[int]) -> None:
        async with self.session() as session:
            user = await session.get(self.model, user.id)
            if user:
                await user.roles.clear()
                for role_id in role_ids:
                    role_obj = await role_controller.get(id=role_id)
                    if role_obj:
                        user.roles.append(role_obj)
                session.add(user)
                await session.commit()

    async def reset_password(self, user_id: int):
        async with self.session() as session:
            user_obj = await session.get(self.model, user_id)
            if user_obj:
                if user_obj.is_superuser:
                    raise HTTPException(status_code=403, detail="Запрещено сбрасывать пароль суперпользователя")
                user_obj.password = get_password_hash(password="123456")
                session.add(user_obj)
                await session.commit()

# Make sure to pass an AsyncSession instance to UserController
user_controller = UserController(session=SessionLocal)
