# base.py: Common LLM client utilities with symbolic resonance integration
import os
import logging
import openai
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError, validator

load_dotenv()
logger = logging.getLogger(__name__)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logger.warning("OPENAI_API_KEY not set; LLMClient will raise on use")
else:
    openai.api_key = api_key

class LLMRequest(BaseModel):
    text: str
    @validator('text')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("text cannot be empty")
        return v

class LLMClient:
    """
    Generic OpenAI ChatCompletion client.
    Automatically manages API key, validation, logging, and symbolic state.
    """
    def __init__(self, system_prompt: str, model: str = "gpt-4", max_tokens: int = 256, temperature: float = 0.7, symbolic_state=None):
        self.system_prompt = system_prompt
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.logger = logger
        self.symbolic_state = symbolic_state

    def chat(self, user_text: str) -> str:
        """Send a chat request and return the assistant's reply."""
        # Validate input
        try:
            req = LLMRequest(text=user_text)
        except ValidationError as e:
            self.logger.error(f"Validation error in LLMRequest: {e}")
            raise
        self.logger.info(f"LLMClient.chat user_text={req.text!r}")
        if self.symbolic_state:
            self.symbolic_state.update(self.__class__.__name__ + ":user_text", req.text)
        try:
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
            self.logger.info(f"LLMClient.chat response received")
            if self.symbolic_state:
                self.symbolic_state.update(self.__class__.__name__ + ":response", content)
            return content
        except Exception:
            self.logger.exception("Error in LLMClient.chat")
            raise