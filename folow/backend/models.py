from sqlalchemy import Column, String, Integer, Date, DateTime
from sqlalchemy.dialects.postgresql import UUID
from database import Base
import uuid
from datetime import datetime

class Customer(Base):
    __tablename__ = "customers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    phone = Column(String(15), nullable=False)
    last_visit = Column(Date, nullable=True)
    next_followup = Column(Date, nullable=True)
    template_name = Column(String(50), nullable=False)
    status = Column(String(20), default="pending")
    retry_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
