from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
# Define allowed origins (you can use "*" to allow all)
origins = [
    "http://localhost:5173"
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,              # or ["*"] for all origins
    allow_credentials=True,
    allow_methods=["*"],                # allows GET, POST, PUT, DELETE, OPTIONS, etc.
    allow_headers=["*"]                 # allows all headers
)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/emails/", response_model=schemas.EmailRequestOut)
def create_email(req: schemas.EmailRequestCreate, db: Session = Depends(get_db)):
    db_req = models.EmailRequest(**req.dict())
    db.add(db_req)
    db.commit()
    db.refresh(db_req)
    return db_req

@app.get("/api/emails/")
def get_all_emails(db: Session = Depends(get_db)):
    emails = db.query(models.EmailRequest).all()
    formatted_emails = []

    print ("Emails Retrieved : ==================", emails)

    try:
        for email in emails:
            print("Email Record : ===============", email)
            original = email.original_email or {}
            formatted = {
                "id": email.request_id,
                "from": original.get("from", ""),
                "subject": original.get("subject", ""),
                "date": original.get("date", ""),
                "body": original.get("body", ""),
                "classification": email.classification_type or "unclassified",
                "businessProcess": email.business_process or "other",
                "extractedData": email.extracted_data or "",
                "automationStatus": email.automation_status,
                "processingStatus": email.processing_status
            }
            formatted_emails.append(formatted)
    except Exception as e:
        print("Error formatting emails:, Exception Stack", e.__traceback__, e)

    return formatted_emails


@app.get("/api/emails/{request_id}", response_model=schemas.EmailRequestOut)
def read_email(request_id: str, db: Session = Depends(get_db)):
    req = db.query(models.EmailRequest).filter_by(request_id=request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    return req

@app.put("/api/emails/{request_id}", response_model=schemas.EmailRequestOut)
def update_email(request_id: str, update: schemas.EmailRequestUpdate, db: Session = Depends(get_db)):
    req = db.query(models.EmailRequest).filter_by(request_id=request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    for key, value in update.dict(exclude_unset=True).items():
        setattr(req, key, value)
    db.commit()
    db.refresh(req)
    return req

@app.delete("/api/emails/{request_id}")
def delete_email(request_id: str, db: Session = Depends(get_db)):
    req = db.query(models.EmailRequest).filter_by(request_id=request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    db.delete(req)
    db.commit()
    return {"detail": "Deleted successfully"}