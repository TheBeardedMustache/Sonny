"""
symbolic_service.py: FastAPI service for symbolic reasoning and Codex AI interactions.
"""
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()
app = FastAPI(title="Sonny Symbolic AI Service", version="1.0")

from backend.core.autonomous_agent import AutonomousAgent

# Robust logger to symbolic_reasoning.log
import os
from datetime import datetime
SYMBOLIC_LOGFILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../logs/symbolic_reasoning.log")
)
def log_symbolic(reason: str, level: str = "INFO"):
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(SYMBOLIC_LOGFILE, "a", encoding="utf-8") as f:
            f.write(f"[{ts}] [SYMBOLIC-AI|{level}] {reason}\n")
    except Exception as exc:
        print(f"SymbolicAI LOG ERROR: {exc} for log line: {reason}")

class SymbolicRequest(BaseModel):
    text: str

@app.on_event("startup")
async def startup_event():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")

# --- Unified symbolic endpoint (single POST) ---
@app.post("/symbolic/")
async def symbolic_endpoint(req: SymbolicRequest):
    """
    Unified endpoint: Accepts a symbolic reasoning request and proxies to Sonny's backend autonomous agent.
    Logs request, explicit tool path, reasoning, and ultimate result.
    """
    log_symbolic(f"API /symbolic/ called with: '{req.text}'")
    try:
        agent = AutonomousAgent(system_prompt="You are Sonny, a robust explicit symbolic autonomy agent for NLU and backend integration.")
        output = agent.reason_decide_act(req.text)
        final_result = output.get("result") or ""
        log_symbolic(f"Symbolic backend result: {final_result[:200]}", level="RESULT")
        return {"result": final_result, "decision": output.get("decision"), "log": output.get("log")}
    except Exception as e:
        log_symbolic(f"Exception in /symbolic/: {str(e)}", level="ERROR")
        raise HTTPException(status_code=400, detail=str(e))