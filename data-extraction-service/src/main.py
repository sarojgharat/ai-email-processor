from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .extractor import DataExtractor  # Adjust import path as needed

app = FastAPI()
extractor = DataExtractor()

# Request schema
class ExtractionRequest(BaseModel):
    process: str
    category: str
    text: str

# Response schema
class ExtractionResponse(BaseModel):
    extracted_data: str

@app.post("/extract", response_model=ExtractionResponse)
def extract_text(request: ExtractionRequest):
    print ("------------------------")
    try:
        result = extractor.extract_text(
            process=request.process,
            category=request.category,
            text=request.text
        )
        print ( f"Extraction result: {result}" )
        return ExtractionResponse(extracted_data=result)
    except Exception as e:
        print (f"Error during extraction: {e} traceback {e.__traceback__}")
        raise HTTPException(status_code=500, detail=str(e))