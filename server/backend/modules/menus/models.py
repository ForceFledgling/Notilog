from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSON

from typing import List

# from backend.core.database import Base
from backend.modules.base.models import BaseModel


class Menu(BaseModel):
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