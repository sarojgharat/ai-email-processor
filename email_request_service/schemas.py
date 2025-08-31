from pydantic import BaseModel
from typing import Optional, Dict, Any

class EmailRequestCreate(BaseModel):
    request_id: str
    business_process: Optional[str]
    original_email: Dict

class EmailRequestUpdate(BaseModel):
    business_process: Optional[str] = None
    classification_type: Optional[str] = None
    extracted_data: Optional[Dict[str, Any]] = None

class EmailRequestOut(BaseModel):
    request_id: str
    business_process: Optional[str]
    classification_type: Optional[str]
    original_email: Optional[Dict]
    extracted_data: Optional[Dict]

    class Config:
        orm_mode = True