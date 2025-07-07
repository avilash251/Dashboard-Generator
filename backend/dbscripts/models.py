from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .base import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(String, nullable=False)
    response_type = Column(String, nullable=False)  # "slm", "gemini", "anomaly"
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_type = Column(String, default="user")
