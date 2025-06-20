"""
llm_client.py

Reusable LLMClient and request validation module extracted from cinnabar logic.
"""
import logging
import openai
from pydantic import BaseModel, validator, ValidationError

logger = logging.getLogger(__name__)

class LLMRequest(BaseModel):
    text: str

    @validator('text')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("text cannot be empty")
        return v

class LLMClient:
    """Generic OpenAI client with validation and logging."""
    def __init__(self, system_prompt: str, model: str = "gpt-4", max_tokens: int = 256, temperature: float = 0.7, symbolic_state=None):
        self.system_prompt = system_prompt
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.symbolic_state = symbolic_state

    def chat(self, user_text: str) -> str:
        try:
            req = LLMRequest(text=user_text)
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            raise
        logger.info(f"LLMClient.chat user_text={req.text!r}")
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": req.text},
            ],
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            n=1,
        )
        content = response.choices[0].message.content
        if self.symbolic_state:
            self.symbolic_state.update("LLMClient:response", content)
        return content