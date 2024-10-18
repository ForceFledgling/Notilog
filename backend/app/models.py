import uuid

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner", cascade_delete=True)
    events: list["Event"] = Relationship(back_populates="owner", cascade_delete=True)


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(max_length=255)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)


class EventBase(SQLModel):
    """
    Базовая схема, которая используется для создания и обновления события.
    Все поля являются необязательными (Optional),
    что позволяет использовать эту схему в других контекстах (например, для обновлений или чтения данных).
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    host: str = Field(max_length=20)                                        # Название или адрес хоста
    source: str = Field(max_length=30)                                      # Сервис или модуль, который сгенерировал лог
    service: str = Field(max_length=30)                                     # Источник лога (приложение, служба или процесс)
    environment: str = Field(max_length=20)                                 # Окружение (production, staging и т.д.)
    context: str | None = Field(default=None)                               # Дополнительные данные (в формате JSON)
    request_id: str | None = Field(default=None, max_length=50)             # Идентификатор запроса
    correlation_id: str | None = Field(default=None, max_length=50)         # Идентификатор для связи логов в рамках процесса
    level: str = Field(max_length=20)                                       # Уровень серьезности (DEBUG, INFO и т.д.)
    stack_trace: str | None = Field(default=None, max_length=1000)                       # Трассировка стека для ошибок
    message: str = Field(max_length=255)                                    # Описание события

# Database model, database table inferred from class name
class Event(EventBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="events")

class EventCreate(EventBase):
    pass

class EventUpdate(EventBase):
    pass

# Properties to return via API, id is always required
class EventPublic(EventBase):
    id: uuid.UUID
    owner_id: uuid.UUID

class EventsPublic(SQLModel):
    data: list[EventPublic]
    count: int