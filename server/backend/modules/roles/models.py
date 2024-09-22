from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSON

from typing import List

# from backend.core.database import Base
from backend.modules.base.models import BaseModel


class Role(BaseModel):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True, index=True)
    desc = Column(String(500), nullable=True)
    
    users = relationship("User", secondary="user_role", back_populates="roles")
