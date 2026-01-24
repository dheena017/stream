import sys
import os
import json
import logging
from loguru import logger
from datetime import datetime

# Define log paths
LOG_DIR = "logs"
APP_LOG_PATH = os.path.join(LOG_DIR, "app.log")
USAGE_LOG_PATH = os.path.join(LOG_DIR, "usage.jsonl")

def init_logging():
    """Initialize the logging configuration."""
    # Create logs directory if it doesn't exist
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    # Remove default handler
    logger.remove()

    # Add console handler (stderr)
    logger.add(sys.stderr, level="INFO")

    # Add file handler for general application logs (readable)
    logger.add(
        APP_LOG_PATH,
        rotation="10 MB",
        retention="10 days",
        compression="zip",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    )

    # Add file handler for usage metrics (JSONL)
    # Filter: only log records that have 'json_data' in extra
    logger.add(
        USAGE_LOG_PATH,
        rotation="10 MB",
        retention="30 days",
        filter=lambda record: "json_data" in record["extra"],
        format="{message}",
        level="INFO"
    )

    # Intercept standard logging messages
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            # Get corresponding Loguru level if it exists
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = record.levelno

            # Find caller from where originated the logged message
            frame, depth = logging.currentframe(), 2
            while frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1

            logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

    # We replace the basicConfig if it was set, but since streamlit runs app.py multiple times,
    # we might need to be careful. However, basicConfig is idempotent if handlers are set?
    # Actually basicConfig does nothing if root logger has handlers.
    # We will clear existing handlers from root logger to be safe.
    logging.getLogger().handlers = [InterceptHandler()]
    logging.getLogger().setLevel(logging.INFO)


def track_request(provider, model, success, latency, token_usage=None, session_id=None):
    """
    Log a structured event for an API request.

    Args:
        provider (str): The AI provider (e.g., 'openai', 'google').
        model (str): The model name used.
        success (bool): Whether the request was successful.
        latency (float): Time taken in seconds.
        token_usage (dict, optional): Token usage stats.
        session_id (str, optional): User session identifier.
    """
    data = {
        "timestamp": datetime.now().isoformat(),
        "type": "api_request",
        "provider": provider,
        "model": model,
        "success": success,
        "latency": latency,
        "token_usage": token_usage,
        "session_id": session_id
    }
    # Bind json_data to extra so the filter catches it
    logger.bind(json_data=True).info(json.dumps(data))

def track_error(error_msg, context=None):
    """
    Log a structured event for an error.
    """
    data = {
        "timestamp": datetime.now().isoformat(),
        "type": "error",
        "error": str(error_msg),
        "context": context
    }
    logger.bind(json_data=True).error(json.dumps(data))

if __name__ == "__main__":
    # Test logging if run directly
    init_logging()
    logger.info("Monitoring module test started")
    track_request("test_provider", "test_model", True, 0.5)
    track_error("Test error", "Testing monitoring module")
    print(f"Logs created in {LOG_DIR}")
