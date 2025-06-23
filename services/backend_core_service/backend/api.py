import os
# api.py: FastAPI endpoints for Sonny platform
import logging
import os
from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services.backend_core_service.backend.core.core_agent import process_request, symbolic_state
import httpx
from services.backend_core_service.backend.core.autonomy import generate_proactive_plan, predict_next_actions

# URL for Symbolic AI microservice
SYMBOLIC_AI_URL = os.getenv("SYMBOLIC_AI_URL", "http://127.0.0.1:8001")

# Explicit logger setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sonny API", version="1.0")
from fastapi.middleware.gzip import GZipMiddleware

# Compress large responses
app.add_middleware(GZipMiddleware, minimum_size=500)

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

class TextRequest(BaseModel):
    text: str

class ScriptRequest(BaseModel):
    prompt: str

@app.get("/")
def read_root():
    """Healthcheck and root endpoint."""
    return {"status": "Sonny API is running"}

@app.get("/state/")
def get_state():
    """Retrieve the current symbolic state."""
    return symbolic_state.get_state()

@app.post("/interpret/")
async def interpret_proxy(req: TextRequest):
    """Proxy to the Symbolic AI service interpret endpoint."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{SYMBOLIC_AI_URL}/interpret/", json=req.dict())
    resp.raise_for_status()
    return resp.json()

@app.post("/respond/")
async def respond_proxy(req: TextRequest):
    """Proxy to the Symbolic AI service respond endpoint."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{SYMBOLIC_AI_URL}/respond/", json=req.dict())
    resp.raise_for_status()
    return resp.json()

@app.post("/script/")
async def script_proxy(req: ScriptRequest):
    """Proxy to the Symbolic AI service script endpoint."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{SYMBOLIC_AI_URL}/script/", json=req.dict())
    resp.raise_for_status()
    return resp.json()

class StateRequest(BaseModel):
    state: dict

@app.post("/autonomy/proactive/")
async def proactive_autonomy(req: StateRequest):
    """Generate proactive task plans based on current state."""
    tasks = generate_proactive_plan(req.state)
    return {"tasks": tasks}

@app.post("/autonomy/predict/")
async def predictive_autonomy(req: StateRequest):
    """Predict next actions based on current state patterns."""
    return predict_next_actions(req.state)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("API_PORT", 8000))
    uvicorn.run("backend.api:app", host="0.0.0.0", port=port)