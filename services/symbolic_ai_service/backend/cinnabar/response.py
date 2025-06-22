# response.py: Generates assistant responses via OpenAI API—Sophic Mercury mode
import os
import logging
from openai import OpenAI
from dotenv import load_dotenv
from backend.core.core_agent import symbolic_state
from pydantic import BaseModel, ValidationError, validator
from backend.cinnabar.advanced import analyze_text
from datetime import datetime

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
    """
    Sophic Mercury: Generate a response with advanced symbolic, chain-of-thought reasoning.
    Results and explanations are appended to the sophic_mercury_integration log.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")
    client = OpenAI(api_key=api_key)
    # Validate input
    try:
        params = ResponseInput(text=text, model=model, max_tokens=max_tokens)
    except ValidationError as e:
        logger.error(f"Validation error in generate_response: {e}")
        raise ValueError(str(e))
    logger.info(f"SophicMercury generating response for input: {params.text}")
    # Sophic Mercury: chain-of-thought and advanced symbolic reasoning steps
    analysis = analyze_text(params.text)
    dt = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    sm_log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../logs/sophic_mercury_integration.log"))
    try:
        with open(sm_log_path, "a", encoding="utf-8") as f:
            f.write(f"[{dt}] [sophic][response] Analysis: {str(analysis)} Text: {params.text}\n")
    except Exception: pass
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a profound symbolic assistant, reasoning as Sophic Mercury."},
                {"role": "assistant", "content": str(analysis)},
                {"role": "user", "content": text},
            ],
            max_tokens=max_tokens,
            temperature=0.7,
            n=1,
        )
        content = response.choices[0].message.content
        symbolic_state.update("sophic_generate_response", {"content": content, "analysis": analysis})
        return content
    except Exception as err:
        logger.exception("Error generating Sophic Mercury response")
        try:
            with open(sm_log_path, "a", encoding="utf-8") as f:
                f.write(f"[{dt}] [sophic][response][ERROR] Exception: {err}\n")
        except Exception: pass
        raise
