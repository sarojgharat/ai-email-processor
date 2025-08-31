from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/email/", response_model=schemas.EmailRequestOut)
def create_email(req: schemas.EmailRequestCreate, db: Session = Depends(get_db)):
    db_req = models.EmailRequest(**req.dict())
    db.add(db_req)
    db.commit()
    db.refresh(db_req)
    return db_req

@app.get("/email/{request_id}", response_model=schemas.EmailRequestOut)
def read_email(request_id: str, db: Session = Depends(get_db)):
    req = db.query(models.EmailRequest).filter_by(request_id=request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    return req

@app.put("/email/{request_id}", response_model=schemas.EmailRequestOut)
def update_email(request_id: str, update: schemas.EmailRequestUpdate, db: Session = Depends(get_db)):
    req = db.query(models.EmailRequest).filter_by(request_id=request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    for key, value in update.dict(exclude_unset=True).items():
        setattr(req, key, value)
    db.commit()
    db.refresh(req)
    return req

@app.delete("/email/{request_id}")
def delete_email(request_id: str, db: Session = Depends(get_db)):
    req = db.query(models.EmailRequest).filter_by(request_id=request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
    db.delete(req)
    db.commit()
    return {"detail": "Deleted successfully"}