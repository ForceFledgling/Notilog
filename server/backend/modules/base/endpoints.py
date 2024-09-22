from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.future import select
from backend.modules.users.controllers import user_controller
from backend.core.ctx import CTX_USER_ID
from backend.core.dependency import DependAuth
from backend.models.admin import Api, Menu, Role, User
from backend.modules.base.schemas import Fail, Success
from backend.modules.login.schemas import CredentialsSchema
from backend.modules.users.schemas import UpdatePassword, BaseUser
from backend.settings import settings
from backend.utils.jwt import create_access_token
from backend.utils.password import get_password_hash, verify_password
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.database import SessionLocal

from backend.modules.login.schemas import JWTOut, JWTPayload

router = APIRouter()

@router.post("/access_token", summary="Получить токен")
async def login_access_token(credentials: CredentialsSchema):
    user = await user_controller.authenticate(credentials)
    await user_controller.update_last_login(user.id)
    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + access_token_expires

    data = JWTOut(
        access_token=create_access_token(
            data=JWTPayload(
                user_id=user.id,
                username=user.username,
                is_superuser=user.is_superuser,
                exp=expire,
            )
        ),
        username=user.username,
    )
    return Success(data=data.model_dump())

@router.get("/userinfo", summary="Получить информацию о пользователе", dependencies=[DependAuth])
async def get_userinfo():
    user_id = CTX_USER_ID.get()
    async with SessionLocal() as session:
        result = await session.execute(select(User).filter_by(id=user_id))
        user_obj = result.scalars().first()
        if user_obj is None:
            return Fail(msg="Пользователь не найден")
        data = await user_obj.to_dict(exclude_fields=["password"])
        data["avatar"] = "https://cdn.jsdelivr.net/gh/alohe/avatars/png/memo_32.png"  # https://github.com/alohe/avatars
        return Success(data=data)

@router.get("/usermenu", summary="Получить меню пользователя", dependencies=[DependAuth])
async def get_user_menu():
    user_id = CTX_USER_ID.get()
    async with SessionLocal() as session:
        result = await session.execute(select(User).filter_by(id=user_id))
        user_obj = result.scalars().first()
        if user_obj is None:
            return Fail(msg="Пользователь не найден")

        menus = []
        if user_obj.is_superuser:
            result = await session.execute(select(Menu))
            menus = result.scalars().all()
        else:
            role_objs = await session.execute(select(Role).join(User.roles).filter_by(id=user_id))
            role_objs = role_objs.scalars().all()
            for role_obj in role_objs:
                result = await session.execute(select(Menu).join(Role.menus).filter_by(id=role_obj.id))
                menus.extend(result.scalars().all())
            menus = list(set(menus))

        parent_menus = [menu for menu in menus if menu.parent_id == 0]
        res = []
        for parent_menu in parent_menus:
            parent_menu_dict = await parent_menu.to_dict()
            parent_menu_dict["children"] = [await menu.to_dict() for menu in menus if menu.parent_id == parent_menu.id]
            res.append(parent_menu_dict)
        return Success(data=res)

@router.get("/userapi", summary="Получить API пользователя", dependencies=[DependAuth])
async def get_user_api():
    user_id = CTX_USER_ID.get()
    async with SessionLocal() as session:
        result = await session.execute(select(User).filter_by(id=user_id))
        user_obj = result.scalars().first()
        if user_obj is None:
            return Fail(msg="Пользователь не найден")

        if user_obj.is_superuser:
            result = await session.execute(select(Api))
            api_objs = result.scalars().all()
            apis = [api.method.lower() + api.path for api in api_objs]
        else:
            role_objs = await session.execute(select(Role).join(User.roles).filter_by(id=user_id))
            role_objs = role_objs.scalars().all()
            apis = []
            for role_obj in role_objs:
                result = await session.execute(select(Api).join(Role.apis).filter_by(id=role_obj.id))
                api_objs = result.scalars().all()
                apis.extend([api.method.lower() + api.path for api in api_objs])
            apis = list(set(apis))

        return Success(data=apis)

@router.post("/update_password", summary="Изменить пароль", dependencies=[DependAuth])
async def update_user_password(req_in: UpdatePassword):
    user_id = CTX_USER_ID.get()
    async with SessionLocal() as session:
        user = await user_controller.get(user_id)
        if user is None:
            return Fail(msg="Пользователь не найден")

        verified = verify_password(req_in.old_password, user.password)
        if not verified:
            return Fail(msg="Ошибка проверки старого пароля!")

        user.password = get_password_hash(req_in.new_password)
        await session.commit()
        return Success(msg="Пароль успешно изменен")
