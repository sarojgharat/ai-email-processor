from sqlalchemy import Column, Text, JSON, TIMESTAMP
from database import Base
from datetime import datetime

class EmailRequest(Base):
    __tablename__ = "email_requests"

    request_id = Column(Text, primary_key=True, index=True)
    business_process = Column(Text)
    classification_type = Column(Text)
    original_email = Column(JSON)
    extracted_data = Column(JSON)
    automation_status = Column(Text)
    processing_status = Column(Text, default="PENDING")
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)