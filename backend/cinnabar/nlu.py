# nlu.py: Natural language understanding utilities via OpenAI API.
import os
import logging
import openai
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

def interpret_input(text: str, model: str = "gpt-4", max_tokens: int = 256) -> str:
    """Interpret user's natural language input and extract intent or structured data."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")
    openai.api_key = api_key
    logger.info(f"Interpreting input: {text}")
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