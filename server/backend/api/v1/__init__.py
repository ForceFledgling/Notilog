from fastapi import APIRouter

from backend.core.dependency import DependPermisson

from backend.modules.apis import apis_router
from backend.modules.base import base_router
from backend.modules.depts import depts_router
from backend.modules.menus import menus_router
from backend.modules.roles import roles_router
from backend.modules.users import users_router
from backend.modules.auditlog import auditlog_router
from backend.modules.events import events_router


v1_router = APIRouter()

v1_router.include_router(base_router, prefix="/base")
v1_router.include_router(users_router, prefix="/user", dependencies=[DependPermisson])
v1_router.include_router(roles_router, prefix="/role", dependencies=[DependPermisson])
v1_router.include_router(menus_router, prefix="/menu", dependencies=[DependPermisson])
v1_router.include_router(apis_router, prefix="/api", dependencies=[DependPermisson])
v1_router.include_router(depts_router, prefix="/dept", dependencies=[DependPermisson])
v1_router.include_router(auditlog_router, prefix="/auditlog", dependencies=[DependPermisson])
v1_router.include_router(events_router, prefix="/event", dependencies=[DependPermisson])
