

# core_utils.py: Stable utility functions for the Sonny backend.

# Load environment variables
import os
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

def helper():
    """Auxiliary helper function."""
    # Check environment variable
    config_value = os.getenv("OTHER_SETTING", "default")
    logger.debug("Helper config OTHER_SETTING: %s", config_value)
    logger.info("Running helper utility")
    try:
        # Utility logic placeholder
        pass
    except Exception:
        logger.exception("Error in helper utility")
        raise
