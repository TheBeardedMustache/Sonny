# api.py: FastAPI endpoints for Sonny platform
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.core.core_agent import process_request

app = FastAPI(title="Sonny API", version="1.0")

@app.on_event("startup")
def on_startup():
    logger.info("Sonny API Service starting up...")

@app.on_event("shutdown")
def on_shutdown():
    logger.info("Sonny API Service shutting down gracefully...")

class ProcessRequest(BaseModel):
    text: str

@app.post("/process/")
def process_endpoint(req: ProcessRequest):
    """Process user text via symbolic reasoning and LLM."""
    result = process_request(req.text)
    if result is None:
        raise HTTPException(status_code=400, detail="Invalid or empty input")
    return {"response": result}
@app.get("/")
def read_root():
    """Healthcheck and root endpoint."""
    return {"status": "Sonny API is running"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("API_PORT", 8000))
    uvicorn.run("backend.api:app", host="0.0.0.0", port=port)