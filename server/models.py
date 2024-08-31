from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from .database import Base  # Используем только Base, который не зависит от SessionLocal

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    level = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
