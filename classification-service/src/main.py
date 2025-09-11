from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .classifier import TextClassifier  # Adjust import path as needed

app = FastAPI()
classifier = TextClassifier()

# Request schema
class ClassificationRequest(BaseModel):
    process: str
    text: str

# Response schema
class ClassificationResponse(BaseModel):
    classification_type: str
    confidence_score: str | None = None

@app.post("/classify", response_model=ClassificationResponse)
def classify_text(request: ClassificationRequest):
    try:
        result = classifier.classify_text(request.process, request.text)
        print (result)
        return ClassificationResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e), traceback=True)