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
logger = logging.getLogger(__name__)


def run_agent():
    """Runs the Sonny agent logic."""
    # Check environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.warning("OPENAI_API_KEY not set; some features may not work")
    else:
        logger.debug("OPENAI_API_KEY successfully loaded")
    logger.info("Starting core agent run")
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
