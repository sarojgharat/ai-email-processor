from pydantic import BaseModel
from typing import Optional, Dict, Any

class EmailRequestCreate(BaseModel):
    request_id: str
    business_process: Optional[str]
    original_email: Dict
    processing_status: Optional[str] = "PENDING"

class EmailRequestUpdate(BaseModel):
    business_process: Optional[str] = None
    classification_type: Optional[str] = None
    extracted_data: Optional[Dict[str, Any]] = None
    automation_status: Optional[str] = None
    processing_status: Optional[str] = None

class EmailRequestOut(BaseModel):
    request_id: str
    business_process: Optional[str]
    classification_type: Optional[str]
    original_email: Optional[Dict]
    extracted_data: Optional[Dict]
    automation_status: Optional[str]
    processing_status: Optional[str]

    class Config:
        orm_mode = True