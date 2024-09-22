from sqlalchemy import Column, Integer, ForeignKey, Table

from backend.modules.base.models import BaseModel


# Association tables for many-to-many relationships
user_role = Table(
    'user_role', BaseModel.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('role_id', Integer, ForeignKey('role.id'))
)

role_menu = Table(
    'role_menu', BaseModel.metadata,
    Column('role_id', Integer, ForeignKey('role.id')),
    Column('menu_id', Integer, ForeignKey('menu.id'))
)

role_api = Table(
    'role_api', BaseModel.metadata,
    Column('role_id', Integer, ForeignKey('role.id')),
    Column('api_id', Integer, ForeignKey('api.id'))
)
