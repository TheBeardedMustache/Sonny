# nlu.py: Natural language understanding utilities via OpenAI API.
import logging
import openai
from backend.cinnabar.base import LLMClient
from backend.core.core_agent import symbolic_state

logger = logging.getLogger(__name__)
# Initialize LLM client for interpretation
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

def interpret_input(text: str) -> str:
    """Interpret user's natural language input and extract intent or structured data."""
    logger.info(f"interpret_input received: {text!r}")
    return _nlu_client.chat(text)