from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import business_process_models, business_process_schemas, database
from fastapi.middleware.cors import CORSMiddleware
from typing import List

# Create all database tables
business_process_models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Business Process Onboarding API",
    description="An API to manage business processes, classification categories, and data extraction formats.",
    version="1.0.0"
)

# Define allowed origins for CORS
origins = [
    "http://localhost:5173",
    "http://localhost:3000", # Add other origins as needed
]

# Add CORS middleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get a database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Business Process Endpoints ---

@app.post("/api/processes/", response_model=business_process_schemas.BusinessProcess, tags=["Business Processes"])
def create_business_process(process: business_process_schemas.BusinessProcessCreate, db: Session = Depends(get_db)):
    """
    Create a new business process.
    """
    db_process = business_process_models.BusinessProcess(name=process.name, description=process.description)
    db.add(db_process)
    db.commit()
    db.refresh(db_process)
    return db_process

@app.get("/api/processes/", response_model=List[business_process_schemas.BusinessProcess], tags=["Business Processes"])
def read_business_processes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all business processes with pagination.
    """
    processes = db.query(business_process_models.BusinessProcess).offset(skip).limit(limit).all()
    return processes

@app.get("/api/processes/{process_id}", response_model=business_process_schemas.BusinessProcess, tags=["Business Processes"])
def read_business_process(process_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single business process by its ID.
    """
    db_process = db.query(business_process_models.BusinessProcess).filter(business_process_models.BusinessProcess.id == process_id).first()
    if db_process is None:
        raise HTTPException(status_code=404, detail="Business Process not found")
    return db_process

@app.put("/api/processes/{process_id}", response_model=business_process_schemas.BusinessProcess, tags=["Business Processes"])
def update_business_process(process_id: int, process: business_process_schemas.BusinessProcessCreate, db: Session = Depends(get_db)):
    """
    Update an existing business process.
    """
    db_process = db.query(business_process_models.BusinessProcess).filter(business_process_models.BusinessProcess.id == process_id).first()
    if db_process is None:
        raise HTTPException(status_code=404, detail="Business Process not found")
    db_process.name = process.name
    db_process.description = process.description
    db.commit()
    db.refresh(db_process)
    return db_process

@app.delete("/api/processes/{process_id}", tags=["Business Processes"])
def delete_business_process(process_id: int, db: Session = Depends(get_db)):
    """
    Delete a business process by its ID.
    """
    db_process = db.query(business_process_models.BusinessProcess).filter(business_process_models.BusinessProcess.id == process_id).first()
    if db_process is None:
        raise HTTPException(status_code=404, detail="Business Process not found")
    db.delete(db_process)
    db.commit()
    return {"detail": "Business Process deleted successfully"}

# --- Classification Category Endpoints ---

@app.post("/api/categories/", response_model=business_process_schemas.ClassificationCategory, tags=["Classification Categories"])
def create_classification_category(category: business_process_schemas.ClassificationCategoryCreate, db: Session = Depends(get_db)):
    """
    Create a new classification category for a business process.
    """
    db_category = business_process_models.ClassificationCategory(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@app.get("/api/processes/{process_id}/categories/", response_model=List[business_process_schemas.ClassificationCategory], tags=["Classification Categories"])
def read_classification_categories_for_process(process_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all classification categories for a specific business process.
    """
    categories = db.query(business_process_models.ClassificationCategory).filter(business_process_models.ClassificationCategory.process_id == process_id).all()
    return categories

# --- Data Extraction Format Endpoints ---

@app.post("/api/formats/", response_model=business_process_schemas.DataExtractionFormat, tags=["Data Extraction Formats"])
def create_data_extraction_format(extraction_format: business_process_schemas.DataExtractionFormatCreate, db: Session = Depends(get_db)):
    """
    Create a new data extraction format for a classification category.
    """
    db_format = business_process_models.DataExtractionFormat(**extraction_format.dict())
    db.add(db_format)
    db.commit()
    db.refresh(db_format)
    return db_format

@app.get("/api/categories/{category_id}/formats/", response_model=List[business_process_schemas.DataExtractionFormat], tags=["Data Extraction Formats"])
def read_data_extraction_formats_for_category(category_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all data extraction formats for a specific classification category.
    """
    formats = db.query(business_process_models.DataExtractionFormat).filter(business_process_models.DataExtractionFormat.category_id == category_id).all()
    return formats
