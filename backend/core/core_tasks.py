# core_tasks.py: Stable core task handling for Sonny.


import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

def handle_task(task):
    """Processes a given task for the Sonny agent."""
    logger.debug("handle_task called with: %s", task)
    logger.info("Handling task: %s", task)
    try:
        # Core task processing placeholder
        pass
    except Exception:
        logger.exception("Error while handling task: %s", task)
        raise
