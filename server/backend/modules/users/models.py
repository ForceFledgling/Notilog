from typing import List
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship

from backend.modules.base.models import BaseModel


class User(BaseModel):
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

