from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSON

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(20), unique=True, index=True)
    alias = Column(String(30), nullable=True, index=True)
    email = Column(String(255), unique=True, index=True)
    phone = Column(String(20), nullable=True, index=True)
    password = Column(String(128), nullable=True)
    is_active = Column(Boolean, default=True, index=True)
    is_superuser = Column(Boolean, default=False, index=True)
    last_login = Column(DateTime, nullable=True, index=True)
    dept_id = Column(Integer, ForeignKey("dept.id"), nullable=True, index=True)
    
    roles = relationship("Role", secondary="user_role", back_populates="users")

class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True, index=True)
    desc = Column(String(500), nullable=True)
    
    users = relationship("User", secondary="user_role", back_populates="roles")
    # menus = relationship("Menu", secondary="role_menu", back_populates="roles")
    # apis = relationship("Api", secondary="role_api", back_populates="roles")

class Api(Base):
    __tablename__ = "api"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String(100), index=True)
    method = Column(String(10), index=True)
    summary = Column(String(500), index=True)
    tags = Column(String(100), index=True)

class Menu(Base):
    __tablename__ = "menu"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), index=True)
    remark = Column(JSON, nullable=True)
    menu_type = Column(String(50), nullable=True)
    icon = Column(String(100), nullable=True)
    path = Column(String(100), index=True)
    order = Column(Integer, default=0, index=True)
    parent_id = Column(Integer, default=0, index=True)
    is_hidden = Column(Boolean, default=False)
    component = Column(String(100))
    keepalive = Column(Boolean, default=True)
    redirect = Column(String(100), nullable=True)

class Dept(Base):
    __tablename__ = "dept"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True, index=True)
    desc = Column(String(500), nullable=True)
    is_deleted = Column(Boolean, default=False, index=True)
    order = Column(Integer, default=0, index=True)
    parent_id = Column(Integer, default=0, index=True)

class DeptClosure(Base):
    __tablename__ = "dept_closure"

    id = Column(Integer, primary_key=True, index=True)
    ancestor = Column(Integer, index=True)
    descendant = Column(Integer, index=True)
    level = Column(Integer, default=0, index=True)

class AuditLog(Base):
    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    username = Column(String(64), default="", index=True)
    module = Column(String(64), default="", index=True)
    summary = Column(String(128), default="", index=True)
    method = Column(String(10), default="", index=True)
    path = Column(String(255), default="", index=True)
    status = Column(Integer, default=-1, index=True)
    response_time = Column(Integer, default=0, index=True)

# Association tables for many-to-many relationships
user_role = Table(
    'user_role', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('role_id', Integer, ForeignKey('role.id'))
)

role_menu = Table(
    'role_menu', Base.metadata,
    Column('role_id', Integer, ForeignKey('role.id')),
    Column('menu_id', Integer, ForeignKey('menu.id'))
)

role_api = Table(
    'role_api', Base.metadata,
    Column('role_id', Integer, ForeignKey('role.id')),
    Column('api_id', Integer, ForeignKey('api.id'))
)
