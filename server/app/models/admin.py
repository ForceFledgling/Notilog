from tortoise import fields

from app.schemas.menus import MenuType

from .base import BaseModel, TimestampMixin
from .enums import MethodType


class User(BaseModel, TimestampMixin):
    username = fields.CharField(max_length=20, unique=True, description="Имя пользователя", index=True)
    alias = fields.CharField(max_length=30, null=True, description="Фамилия", index=True)
    email = fields.CharField(max_length=255, unique=True, description="Электронная почта", index=True)
    phone = fields.CharField(max_length=20, null=True, description="Телефон", index=True)
    password = fields.CharField(max_length=128, null=True, description="Пароль")
    is_active = fields.BooleanField(default=True, description="Активен", index=True)
    is_superuser = fields.BooleanField(default=False, description="Суперпользователь", index=True)
    last_login = fields.DatetimeField(null=True, description="Дата последнего входа", index=True)
    roles = fields.ManyToManyField("models.Role", related_name="user_roles")
    dept_id = fields.IntField(null=True, description="ID отдела", index=True)

    class Meta:
        table = "user"

    class PydanticMeta:
        # todo
        # computed = ["full_name"]
        ...


class Role(BaseModel, TimestampMixin):
    name = fields.CharField(max_length=20, unique=True, description="Название роли", index=True)
    desc = fields.CharField(max_length=500, null=True, blank=True, description="Описание роли")
    menus = fields.ManyToManyField("models.Menu", related_name="role_menus")
    apis = fields.ManyToManyField("models.Api", related_name="role_apis")

    class Meta:
        table = "role"


class Api(BaseModel, TimestampMixin):
    path = fields.CharField(max_length=100, description="Путь API", index=True)
    method = fields.CharEnumField(MethodType, description="Метод запроса", index=True)
    summary = fields.CharField(max_length=500, description="Описание запроса", index=True)
    tags = fields.CharField(max_length=100, description="Теги API", index=True)

    class Meta:
        table = "api"


class Menu(BaseModel, TimestampMixin):
    name = fields.CharField(max_length=20, description="Название меню", index=True)
    remark = fields.JSONField(null=True, description="Резервное поле", blank=True)
    menu_type = fields.CharEnumField(MenuType, null=True, blank=True, description="Тип меню")
    icon = fields.CharField(max_length=100, null=True, blank=True, description="Иконка меню")
    path = fields.CharField(max_length=100, description="Путь меню", index=True)
    order = fields.IntField(default=0, description="Порядок", index=True)
    parent_id = fields.IntField(default=0, max_length=10, description="ID родительского меню", index=True)
    is_hidden = fields.BooleanField(default=False, description="Скрыто")
    component = fields.CharField(max_length=100, description="Компонент")
    keepalive = fields.BooleanField(default=True, description="Сохранить")
    redirect = fields.CharField(max_length=100, null=True, blank=True, description="Перенаправление")

    class Meta:
        table = "menu"


class Dept(BaseModel, TimestampMixin):
    name = fields.CharField(max_length=20, unique=True, description="Название отдела", index=True)
    desc = fields.CharField(max_length=500, null=True, blank=True, description="Примечание")
    is_deleted = fields.BooleanField(default=False, description="Метка мягкого удаления", index=True)
    order = fields.IntField(default=0, description="Порядок", index=True)
    parent_id = fields.IntField(default=0, max_length=10, description="ID родительского отдела", index=True)

    class Meta:
        table = "dept"


class DeptClosure(BaseModel, TimestampMixin):
    ancestor = fields.IntField(description="Предок", index=True)
    descendant = fields.IntField(description="Потомок", index=True)
    level = fields.IntField(default=0, description="Уровень", index=True)


class AuditLog(BaseModel, TimestampMixin):
    user_id = fields.IntField(description="ID пользователя", index=True)
    username = fields.CharField(max_length=64, default="", description="Имя пользователя", index=True)
    module = fields.CharField(max_length=64, default="", description="Модуль функции", index=True)
    summary = fields.CharField(max_length=128, default="", description="Описание запроса", index=True)
    method = fields.CharField(max_length=10, default="", description="Метод запроса", index=True)
    path = fields.CharField(max_length=255, default="", description="Путь запроса", index=True)
    status = fields.IntField(default=-1, description="Код статуса", index=True)
    response_time = fields.IntField(default=0, description="Время отклика (в мс)", index=True)
