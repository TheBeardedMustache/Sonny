# nlu.py: Natural language understanding utilities via OpenAI API.
import os
import logging
import openai
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)
from pydantic import BaseModel, ValidationError, validator

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
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")
    openai.api_key = api_key
    # Validate input
    try:
        params = NLUInput(text=text, model=model, max_tokens=max_tokens)
    except ValidationError as e:
        logger.error(f"Validation error in interpret_input: {e}")
        raise
    logger.info(f"Interpreting input: {params.text}")
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant for interpreting user commands."},
                {"role": "user", "content": text},
            ],
            max_tokens=max_tokens,
            temperature=0.0,
            n=1,
        )
        return response.choices[0].message.content
    except Exception:
        logger.exception("Error interpreting input")
        raise