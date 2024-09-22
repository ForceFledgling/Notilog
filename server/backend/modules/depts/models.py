from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSON

from typing import List

# from backend.core.database import Base
from backend.modules.base.models import BaseModel


class Dept(BaseModel):
    __tablename__ = "dept"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True, index=True)
    desc = Column(String(500), nullable=True)
    is_deleted = Column(Boolean, default=False, index=True)
    order = Column(Integer, default=0, index=True)
    parent_id = Column(Integer, default=0, index=True)

class DeptClosure(BaseModel):
    __tablename__ = "dept_closure"

    id = Column(Integer, primary_key=True, index=True)
    ancestor = Column(Integer, index=True)
    descendant = Column(Integer, index=True)
    level = Column(Integer, default=0, index=True)