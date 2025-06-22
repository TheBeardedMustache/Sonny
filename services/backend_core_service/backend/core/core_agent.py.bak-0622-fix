# core_agent.py: Stable core Sonny AI agent functionality.
# Load environment variables
import os
from dotenv import load_dotenv

load_dotenv()

# Logging setup
import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
# Pydantic validation for process_request
from pydantic import BaseModel, ValidationError, validator

logger = logging.getLogger(__name__)

class RequestInput(BaseModel):
    text: str
    @validator('text')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("text cannot be empty")
        return v
# Symbolic reasoning state
class SymbolicState:
    """Tracks symbolic resonance state across operations."""
    def __init__(self):
        self.state = {}

    def update(self, event: str, data):
        """Record an event with associated data."""
        self.state[event] = data
        logger.info(f"SymbolicState updated: {event} = {data}")

    def get_state(self):
        """Retrieve a copy of the symbolic state."""
        return dict(self.state)

symbolic_state = SymbolicState()


def run_agent():
    """Runs the Sonny agent logic."""
    # Check environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.warning("OPENAI_API_KEY not set; some features may not work")
    else:
        logger.debug("OPENAI_API_KEY successfully loaded")
    logger.info("Starting core agent run")
    # Update symbolic resonance
    symbolic_state.update("run_agent", None)
    try:
        # Core agent logic placeholder
        pass
    except Exception:
        logger.exception("Error running core agent logic")
        raise
        
class SilverAutomation:
    """Wrapper class for desktop automation (Silver Path)."""

    def __init__(self):
        self.logger = logger

    def move_mouse(self, x, y, duration=0):
        """Move mouse cursor to (x, y)."""
        self.logger.info(f"SilverAutomation.move_mouse to ({x}, {y})")
        from backend.core.core_tasks import move_mouse
        return move_mouse(x, y, duration=duration)

    def click(self, x=None, y=None, button='left'):
        """Click mouse at (x, y)."""
        self.logger.info(f"SilverAutomation.click at ({x}, {y}) button={button}")
        from backend.core.core_tasks import click
        return click(x, y, button=button)

    def drag_mouse(self, x, y, duration=0):
        """Drag mouse cursor to (x, y)."""
        self.logger.info(f"SilverAutomation.drag_mouse to ({x}, {y})")
        from backend.core.core_tasks import drag_mouse
        return drag_mouse(x, y, duration=duration)

    def type_text(self, text, interval=0):
        """Type text string."""
        self.logger.info(f"SilverAutomation.type_text '{text}'")
        from backend.core.core_tasks import type_text
        return type_text(text, interval=interval)

    def press_keys(self, *keys):
        """Press key combinations."""
        self.logger.info(f"SilverAutomation.press_keys {keys}")
        from backend.core.core_tasks import press_keys
        return press_keys(*keys)

    def open_application(self, path):
        """Open an application by path."""
        self.logger.info(f"SilverAutomation.open_application {path}")
        from backend.core.core_tasks import open_application
        return open_application(path)

    def manage_window(self, action, window_title=None):
        """Manage OS window."""
        self.logger.info(f"SilverAutomation.manage_window action={action}, title={window_title}")
        from backend.core.core_tasks import manage_window
        return manage_window(action, window_title)

# Gold Path: Autonomous code generation via Codex CLI
class GoldAutomation:
    """Wrapper for autonomous code generation via Codex CLI (Gold Path)."""

    def __init__(self):
        self.logger = logger

    def generate_script(self, prompt: str, model: str = "gpt-4", max_tokens: int = 1024) -> str:
        """Generate a new Python script based on prompt."""
        self.logger.info(f"GoldAutomation.generate_script prompt={prompt!r}")
        from backend.core.codex_auto import generate_script as _gen
        try:
            return _gen(prompt, model=model, max_tokens=max_tokens)
        except Exception:
            self.logger.exception("GoldAutomation.generate_script failed")
            raise

    def modify_script(self, file_path: str, instructions: str, model: str = "gpt-4", max_tokens: int = 1024) -> None:
        """Modify an existing Python script per instructions."""
        self.logger.info(f"GoldAutomation.modify_script file={file_path}, instructions={instructions!r}")
        from backend.core.codex_auto import modify_script as _mod
        try:
            return _mod(file_path, instructions, model=model, max_tokens=max_tokens)
        except Exception:
            self.logger.exception("GoldAutomation.modify_script failed")
            raise

    def run_codex_cli(self, command: list, cwd: str = None):
        """Execute a Codex CLI command via subprocess."""
        self.logger.info(f"GoldAutomation.run_codex_cli command={command}")
        from backend.core.codex_auto import run_codex_cli as _run
        try:
            return _run(command, cwd=cwd)
        except Exception:
            self.logger.exception("GoldAutomation.run_codex_cli failed")
            raise

# Mercury & Cinnabar Integration
import backend.cinnabar.nlu as nlu
import backend.cinnabar.response as response

def process_request(text: str) -> str:
    """Unified reasoning for process_request: interpret, reason, and respond with explicit logging."""
    from backend.core.autonomous_agent import AutonomousAgent
    logger.info(f"process_request received: {text}")
    try:
        data = RequestInput(text=text)
        symbolic_state.update("process_request_input", data.text)
    except ValidationError as e:
        logger.error(f"Validation error in process_request: {e}")
        return None
    try:
        agent = AutonomousAgent(system_prompt="You are Sonny, clearly explain decisions, pick best tool, and log all steps.")
        output = agent.reason_decide_act(data.text)
        # Update symbolic resonance, return summary response
        response_log = "\n".join([f"[log] {step}" for step in output["log"]])
        response_log += f"\n[Sonny Action: {output['decision']}]\n{output['result']}"
        symbolic_state.update("process_request_response_log", response_log)
        return response_log
    except Exception as e:
        logger.exception(f"Error processing request autonomously: {e}")
        raise
    
class AnimatedMercury:
    """Dynamic autonomous agent with proactive task generation and symbolic integration."""

    def __init__(self, llm_client=None, symbolic_state=None):
        from backend.cinnabar.base import LLMClient
        # Use provided LLM client or default for symbolic reasoning
        self.llm = llm_client or LLMClient(
            system_prompt="You are an autonomous agent generating proactive tasks.",
            symbolic_state=symbolic_state or globals().get('symbolic_state')
        )
        self.state = symbolic_state or globals().get('symbolic_state')

    def generate_proactive_task(self) -> str:
        """Generate a proactive task based on current symbolic state."""
        # Extract current state snapshot
        current_state = self.state.get_state() if self.state else {}
        prompt = f"Given the current symbolic state: {current_state}, suggest the next best action as a Python instruction."
        logger.info(f"AnimatedMercury generating proactive task with prompt: {prompt}")
        try:
            task = self.llm.chat(prompt)
            # Record in symbolic state
            if self.state:
                self.state.update("proactive_task", task)
            return task
        except Exception:
            logger.exception("Error generating proactive task")
            raise
