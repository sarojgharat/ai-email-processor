# mcp_server.py
from fastapi import FastAPI, Request
from pydantic import BaseModel
from .classifier import classify_text

app = FastAPI()

class MCPMessage(BaseModel):
    context: dict
    payload: dict

@app.post("/mcp/classify")
async def mcp_classify(message: MCPMessage):
    context = message.context
    text = message.payload.get("text", "")
    
    result = classify_text(text)
    
    return {
        "context": context,
        "classification": {
            "label": result["label"],
            "score": round(result["score"], 4)
        }
    }