from pydantic import BaseModel
from typing import List, Optional, Any

# --- Data Extraction Format Schemas ---

class DataExtractionFormatBase(BaseModel):
    format_name: str
    format_definition: Any # Can be a dict or a more complex Pydantic model

class DataExtractionFormatCreate(DataExtractionFormatBase):
    category_id: int

class DataExtractionFormat(DataExtractionFormatBase):
    id: int
    category_id: int

    class Config:
        orm_mode = True

# --- Classification Category Schemas ---

class ClassificationCategoryBase(BaseModel):
    name: str

class ClassificationCategoryCreate(ClassificationCategoryBase):
    process_id: int

class ClassificationCategory(ClassificationCategoryBase):
    id: int
    process_id: int
    data_extraction_formats: List[DataExtractionFormat] = []

    class Config:
        orm_mode = True

# --- Business Process Schemas ---

class BusinessProcessBase(BaseModel):
    name: str
    description: Optional[str] = None

class BusinessProcessCreate(BusinessProcessBase):
    pass

class BusinessProcess(BusinessProcessBase):
    id: int
    classification_categories: List[ClassificationCategory] = []

    class Config:
        orm_mode = True
