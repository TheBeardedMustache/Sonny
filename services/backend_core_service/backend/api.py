# api.py: FastAPI endpoints for Sonny platform
import logging
import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.core.core_agent import process_request

# Explicit logger setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sonny API", version="1.0")

@app.on_event("startup")
async def startup_event():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY missing")
        raise ValueError("OPENAI_API_KEY not set")
    logger.info("Backend service initialized successfully.")

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