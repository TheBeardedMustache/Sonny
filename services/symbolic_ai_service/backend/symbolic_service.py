"""
symbolic_service.py: FastAPI service for symbolic reasoning and Codex AI interactions.
"""
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()
app = FastAPI(title="Sonny Symbolic AI Service", version="1.0")

from backend.cinnabar.nlu import interpret_input
from backend.cinnabar.response import generate_response
from backend.core.codex_auto import generate_script, modify_script
from backend.cinnabar.advanced import analyze_text, plan_tasks, retrieve_memory

class TextRequest(BaseModel):
    text: str

class ScriptRequest(BaseModel):
    prompt: str

@app.on_event("startup")
async def startup_event():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")

@app.post("/interpret/")
async def interpret_endpoint(req: TextRequest):
    """Interpret user text to intent."""
    try:
        intent = interpret_input(req.text)
        return {"intent": intent}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/respond/")
async def respond_endpoint(req: TextRequest):
    """Generate assistant response to text."""
    try:
        resp = generate_response(req.text)
        return {"response": resp}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/script/")
async def script_endpoint(req: ScriptRequest):
    """Generate Python script from prompt."""
    try:
        code = generate_script(req.prompt)
        return {"code": code}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/analyze/")
async def analyze_endpoint(req: TextRequest):
    """Perform advanced symbolic analysis on input text."""
    try:
        result = analyze_text(req.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/plan/")
async def plan_endpoint():
    """Generate proactive task plan based on current symbolic state."""
    try:
        # import here to avoid circular dependency
        from backend.core.core_agent import symbolic_state
        state = symbolic_state.get_state()
        tasks = plan_tasks(state)
        return {"tasks": tasks}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/memory/")
async def memory_endpoint(key: str):
    """Retrieve stored memory fragment by key."""
    try:
        mem = retrieve_memory(key)
        return mem
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))