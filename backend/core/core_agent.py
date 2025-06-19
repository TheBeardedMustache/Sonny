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
