# nlu.py: Natural language understanding utilities via OpenAI API.
def interpret_input(text: str, model: str = "gpt-4", max_tokens: int = 256) -> str:
# Streamlined NLU for Symbolic AI Service
import os
import logging
from datetime import datetime
from openai import OpenAI
from pydantic import BaseModel, validator, ValidationError
from backend.cinnabar.base import LLMClient
from backend.core.core_agent import symbolic_state

# Explicit log setup
LOGFILE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../logs/symbolic_reasoning.log")
)
def log_symbolic(reason: str):
    ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(LOGFILE, "a", encoding="utf-8") as f:
            f.write(f"[{ts}] {reason}\n")
    except Exception as exc:
        # fallback: print if log file not writable
        print(f"SymbolicAI LOG ERROR: {exc} for log line: {reason}")

# LLM client for interpretation
_nlu_client = LLMClient(
    system_prompt="You are a helpful assistant for interpreting user commands.",
    model="gpt-4",
    max_tokens=256,
    temperature=0.0,
    symbolic_state=symbolic_state,
)

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

def interpret_input(text: str, model: str = "gpt-4", max_tokens: int = 256) -> str:
    """Streamlined: interpret user's input and extract intent, explicitly logging each step."""
    log_symbolic(f"interpret_input received: '{text}' [model={model}, max_tokens={max_tokens}]")
    # Validate input
    try:
        data = NLUInput(text=text, model=model, max_tokens=max_tokens)
        log_symbolic(f"Valid input accepted: '{data.text}'")
    except ValidationError as e:
        log_symbolic(f"Validation error: {e}")
        raise ValueError(str(e))
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        log_symbolic("Error: OPENAI_API_KEY not set")
        raise RuntimeError("OPENAI_API_KEY not set")
    client = OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": _nlu_client.system_prompt},
                {"role": "user", "content": data.text},
            ],
            max_tokens=max_tokens,
            n=1,
            temperature=_nlu_client.temperature,
        )
        content = response.choices[0].message.content
        log_symbolic(f"LLM output for '{text}': {content[:200]}")
    except Exception as ex:
        log_symbolic(f"Exception when querying LLM: {ex}")
        raise
    symbolic_state.update("interpret_input", content)
    log_symbolic(f"Symbolic state updated. Output: {content[:120]}")
    return content