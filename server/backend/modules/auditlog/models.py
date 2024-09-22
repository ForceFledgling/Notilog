from sqlalchemy import Column, Integer, String

from backend.modules.base.models import BaseModel


class AuditLog(BaseModel):
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
