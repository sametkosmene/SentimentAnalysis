# src/utils/logging_util.py

import logging
import os

def setup_logging(log_file="app.log", log_level=logging.INFO):
    """
    Setup logging configuration.
    :param log_file: The file where logs will be saved.
    :param log_level: The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    """
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

    # Log the start of the application
    logging.info("Logging is set up.")


# Example usage
if __name__ == "__main__":
    # Setup logging
    setup_logging(log_file="logs/app.log", log_level=logging.DEBUG)

    # Create a logger
    logger = logging.getLogger(__name__)

    # Log some messages
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")
