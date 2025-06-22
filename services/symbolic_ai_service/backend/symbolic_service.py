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
from backend.cinnabar.maturity import contextual_understanding, handle_complex_query, nuanced_response

# Symbolic logger for main endpoint
import logging
import os
from datetime import datetime
SYMBOLIC_LOGFILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../logs/symbolic_reasoning.log")
)
def log_symbolic(reason: str):
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(SYMBOLIC_LOGFILE, "a", encoding="utf-8") as f:
            f.write(f"[{ts}] {reason}\n")
    except Exception as exc:
        print(f"SymbolicAI LOG ERROR: {exc} for log line: {reason}")

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
    """Interpret user text to intent (clearly and robustly logged)."""
    log_symbolic(f"API /interpret/ called with: '{req.text}'")
    try:
        intent = interpret_input(req.text)
        log_symbolic(f"interpret_input result: {intent[:200]}")
        return {"intent": intent}
    except Exception as e:
        log_symbolic(f"Exception in /interpret/: {str(e)}")
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

class ContextualRequest(BaseModel):
    text: str
    history: list

class ComplexQueryRequest(BaseModel):
    query: str
    context: dict

class NuanceRequest(BaseModel):
    text: str
    tone: str = "neutral"

@app.post("/contextual/")
async def contextual_endpoint(req: ContextualRequest):
    """Perform contextual understanding based on conversation history."""
    try:
        return contextual_understanding(req.text, req.history)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/complex_query/")
async def complex_query_endpoint(req: ComplexQueryRequest):
    """Handle complex multi-step queries with advanced reasoning."""
    try:
        return handle_complex_query(req.query, req.context)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/nuanced_respond/")
async def nuanced_endpoint(req: NuanceRequest):
    """Generate a nuanced response with specified tone modulation."""
    try:
        return nuanced_response(req.text, req.tone)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))