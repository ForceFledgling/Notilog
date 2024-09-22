from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import JSON

from typing import List

# from backend.core.database import Base
from backend.modules.base.models import BaseModel


class Api(BaseModel):
    __tablename__ = "api"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String(100), index=True)
    method = Column(String(10), index=True)
    summary = Column(String(500), index=True)
    tags = Column(String(100), index=True)