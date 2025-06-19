# response.py: Generates assistant responses via OpenAI API.
import os
import logging
import openai
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

def generate_response(text: str, model: str = "gpt-4", max_tokens: int = 512) -> str:
    """Generate a response to the user's text input."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")
    openai.api_key = api_key
    logger.info(f"Generating response for input: {text}")
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
        return response.choices[0].message.content
    except Exception:
        logger.exception("Error generating response")
        raise