# base.py: Common LLM client utilities with symbolic resonance integration
import os
import logging
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError, validator

load_dotenv()
logger = logging.getLogger(__name__)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    logger.warning("OPENAI_API_KEY not set; LLMClient will raise on use")
    client = None
else:
    client = OpenAI(api_key=api_key)

class LLMRequest(BaseModel):
    text: str
    @validator('text')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("text cannot be empty")
        return v

class LLMClient:
    def with_history_context(self, user_text: str, history_method: str = "recent", n: int = 3) -> str:
        """Augmented chat: prepend N hits from history as system/user/assistant, before main system/user query."""
        from services.symbolic_ai_service.backend.core import chat_history_kb
        if history_method == "search":
            hist_msgs = chat_history_kb.search_context(user_text, n=n)
        else:
            hist_msgs = chat_history_kb.last_n_turns(n)
        # Compose messages: previous context (role, content), then actual system/user
        context_msgs = [
            {"role": m["role"], "content": f"[{m['conversation']}] {m['content']}"}
            for m in hist_msgs if m["content"].strip()
        ]
        main_msgs = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_text},
        ]
        msgs = context_msgs + main_msgs
        model_id = self.model
        temperature = self.temperature
        response = client.chat.completions.create(
            model=model_id,
            messages=msgs,
            max_tokens=self.max_tokens,
            temperature=temperature,
            n=1,
        )
        content = response.choices[0].message.content
        if self.symbolic_state:
            self.symbolic_state.update(self.__class__.__name__ + ":response", content)
        return content
    """
    Generic OpenAI ChatCompletion client.
    Automatically manages API key, validation, logging, and symbolic state.
    """
    def __init__(self, system_prompt: str, model: str = "ft:gpt-4o-2024-08-06:churchofadeptus:sonny-philosophersstone-v1:BlRr0kpo", max_tokens: int = 256, temperature: float = 0.7, symbolic_state=None):
        self.system_prompt = system_prompt
        # Use fine-tuned model by default; override as needed.
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.logger = logger
        self.symbolic_state = symbolic_state

    def chat(self, user_text: str, model: str = None, temperature: float = None) -> str:
        """Send a chat request (default: fine-tuned model). Optionally override model/temperature per call."""
        # Validate input
        try:
            req = LLMRequest(text=user_text)
        except ValidationError as e:
            self.logger.error(f"Validation error in LLMRequest: {e}")
            raise
        self.logger.info(f"LLMClient.chat user_text={req.text!r}")
        if self.symbolic_state:
            self.symbolic_state.update(self.__class__.__name__ + ":user_text", req.text)
        model_id = model if model is not None else self.model
        temperature = self.temperature if temperature is None else temperature
        try:
            response = client.chat.completions.create(
                model=model_id,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": req.text},
                ],
                max_tokens=self.max_tokens,
                temperature=temperature,
                n=1,
            )
            content = response.choices[0].message.content
            self.logger.info(f"LLMClient.chat response received (model={model_id})")
            if self.symbolic_state:
                self.symbolic_state.update(self.__class__.__name__ + ":response", content)
            return content
        except Exception:
            self.logger.exception("Error in LLMClient.chat")
            raise