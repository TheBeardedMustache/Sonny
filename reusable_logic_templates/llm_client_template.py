"""
llm_client_template.py

Template for LLMClient and LLMRequest:
Encapsulates OpenAI ChatCompletion calls with Pydantic validation and logging.

Usage Example:
```python
from llm_client_template import LLMClient

state = SymbolicState()  # optional, for symbolic resonance
client = LLMClient(
    system_prompt="You are an assistant.",
    model="gpt-4",
    max_tokens=256,
    temperature=0.2,
    symbolic_state=state,
)
response = client.chat("Generate Python code to greet a user.")
print(response)
``` 
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
    """
    Generic OpenAI ChatCompletion client with validation and logging.
    """
    def __init__(
        self,
        system_prompt: str,
        model: str = "gpt-4",
        max_tokens: int = 256,
        temperature: float = 0.7,
        symbolic_state=None,
    ):
        self.system_prompt = system_prompt
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.symbolic_state = symbolic_state

    def chat(self, user_text: str) -> str:
        """Send a chat request and return the assistant's reply."""
        try:
            req = LLMRequest(text=user_text)
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            raise

        logger.info(f"LLMClient.chat user_text={req.text!r}")
        if self.symbolic_state:
            self.symbolic_state.update("LLMClient:user_text", req.text)
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
        logger.info("LLMClient.chat response received")
        if self.symbolic_state:
            self.symbolic_state.update("LLMClient:response", content)
        return content