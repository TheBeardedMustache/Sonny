"""
symbolic_service.py: FastAPI service for symbolic reasoning and Codex AI interactions.
"""
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

load_dotenv()
app = FastAPI(title="Sonny Symbolic AI Service", version="1.0")

from backend.cinnabar.nlu import interpret_input
from backend.cinnabar.response import generate_response
from backend.core.codex_auto import generate_script, modify_script

@app.on_event("startup")
async def startup_event():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")

@app.post("/interpret/")
async def interpret_endpoint(text: str):
    """Interpret user text to intent."""
    try:
        intent = interpret_input(text)
        return {"intent": intent}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/respond/")
async def respond_endpoint(text: str):
    """Generate assistant response to text."""
    try:
        resp = generate_response(text)
        return {"response": resp}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/script/")
async def script_endpoint(prompt: str):
    """Generate Python script from prompt."""
    try:
        code = generate_script(prompt)
        return {"code": code}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))