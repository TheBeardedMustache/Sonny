# nlu.py: Advanced symbolic NLU for Sonny — Sophic Mercury integration
import os
from pydantic import BaseModel, validator, ValidationError
from backend.cinnabar.base import LLMClient, log_symbolic
from backend.core.core_agent import symbolic_state
from backend.cinnabar.advanced import analyze_text, plan_tasks
from datetime import datetime

class NLUInput(BaseModel):
    text: str
    model: str = "gpt-4"
    max_tokens: int = 256
    @validator('text')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("text cannot be empty")
        return v
    @validator('max_tokens')
    def positive_tokens(cls, v):
        if v <= 0:
            raise ValueError("max_tokens must be positive")
        return v

_nlu_client = LLMClient(
    system_prompt="You are a helpful symbolic NLU model enabling Sonny's step-by-step autonomy. Inject rationale for every Caelus-related task (Sophic Mercury mode).",
    model="gpt-4",
    max_tokens=256,
    temperature=0.0,
    symbolic_state=symbolic_state,
)

def interpret_input(text: str, model: str = "gpt-4", max_tokens: int = 256) -> str:
    """
    Advanced symbolic NLU interpretation (Sophic Mercury mode):
     - Chain-of-thought, deep symbolic, and real-time loggable explanation.
     - All plans, analysis, COT, and outputs explicitly logged.
    """
    try:
        data = NLUInput(text=text, model=model, max_tokens=max_tokens)
        log_symbolic(f"interpret_input accepted: '{data.text}' (model={data.model}, max_tokens={data.max_tokens})")
    except ValidationError as e:
        log_symbolic(f"interpret_input validation error: {e}", level="ERROR")
        raise ValueError(str(e))
    # Sophic Mercury: deep symbolic analysis
    analysis = analyze_text(data.text)
    plans = plan_tasks(symbolic_state.get_state())
    # Log all to symbolic_reasoning.log
    log_symbolic(f"[SOPHIC] Sophic analysis: {analysis.get('analysis','')}")
    log_symbolic(f"[SOPHIC] Sophic plans: {plans}")
    # Sophic log file append (for cross-stack auditing)
    dt = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    sm_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../logs/sophic_mercury_integration.log"))
    try:
        with open(sm_path, "a", encoding="utf-8") as f:
            f.write(f"[{dt}] [sophic][nlu] Analysis: {analysis} Plans: {plans} Text: {data.text}\n")
    except Exception: pass
    # Attach explanation and COT to user text for LLM
    context_info = f"[ANALYSIS]: {analysis.get('analysis', '')}\n[COT]: {analysis.get('chain_of_thought', [])}\n[PLANS]: {plans}\n{data.text}"
    result = _nlu_client.chat(context_info)
    symbolic_state.update("sophic_interpret_input", {
        "result": result, "analysis": analysis, "plans": plans
    })
    log_symbolic(f"[SOPHIC] interpret_input symbolic_state updated. Output: {result[:120]}")
    return result
