# nlu.py: Natural language understanding utilities via OpenAI API.
import logging
import os
from openai import OpenAI
from pydantic import BaseModel, validator, ValidationError
from services.backend_core_service.backend.cinnabar.base import LLMClient
from services.backend_core_service.backend.core.core_agent import symbolic_state

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

def interpret_input(text: str, model: str = "gpt-4", max_tokens: int = 256) -> str:
    """Interpret user's natural language input and extract intent or structured data."""
    # Validate input parameters
    try:
        data = NLUInput(text=text, model=model, max_tokens=max_tokens)
    except ValidationError as e:
        logger.error(f"Validation error in interpret_input: {e}")
        raise ValueError(str(e))
    # Ensure API key is set before calling OpenAI
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY not set")
    logger.info(f"interpret_input received: {data.text!r}")
    # Perform interpretation via OpenAI API using new SDK
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
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
    except Exception:
        logger.exception("Error interpreting input")
        raise
    symbolic_state.update("interpret_input", content)
    return content