# response.py: Generates assistant responses via OpenAI API.
import os
import logging
import openai
from dotenv import load_dotenv
from backend.core.core_agent import symbolic_state
from pydantic import BaseModel, ValidationError, validator

class ResponseInput(BaseModel):
    text: str
    model: str = "gpt-4"
    max_tokens: int = 512

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

load_dotenv()
logger = logging.getLogger(__name__)

def generate_response(text: str, model: str = "gpt-4", max_tokens: int = 512) -> str:
    """Generate a response to the user's text input."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")
    openai.api_key = api_key
    # Validate input
    try:
        params = ResponseInput(text=text, model=model, max_tokens=max_tokens)
    except ValidationError as e:
        logger.error(f"Validation error in generate_response: {e}")
        raise ValueError(str(e))
    logger.info(f"Generating response for input: {params.text}")
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant responding to user queries."},
                {"role": "user", "content": text},
            ],
            max_tokens=max_tokens,
            temperature=0.7,
            n=1,
        )
        content = response.choices[0].message.content
        symbolic_state.update("generate_response", content)
        return content
    except Exception:
        logger.exception("Error generating response")
        raise