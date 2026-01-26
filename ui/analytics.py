import sys
import os
from loguru import logger

# Ensure logs directory exists
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "app.log")

def configure_logging():
    """Configures the logger with console and file handlers."""
    # Remove default handler to avoid duplicate logs if re-imported
    logger.remove()

    # Add console handler
    logger.add(sys.stderr, level="INFO", format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")

    # Add file handler with rotation and retention, utilizing JSON serialization for analytics
    logger.add(
        LOG_FILE,
        rotation="10 MB",
        retention="7 days",
        level="DEBUG",
        serialize=True,
        enqueue=True
    )

def log_api_call(provider: str, model: str, duration: float, success: bool, input_tokens: int = 0, output_tokens: int = 0, error: str = None):
    """
    Logs an API call with structured data.

    Args:
        provider: The name of the AI provider (e.g., 'openai', 'anthropic').
        model: The specific model used.
        duration: Time taken for the call in seconds.
        success: Whether the call was successful.
        input_tokens: Number of input tokens (estimated or actual).
        output_tokens: Number of output tokens.
        error: Error message if any.
    """
    logger.bind(
        event_type="api_call",
        provider=provider,
        model=model,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        duration=duration,
        success=success,
        error=error
    ).info(f"API Call to {provider} ({model}) - Success: {success}")

def log_error(context: str, error_message: str, exception: Exception = None):
    """
    Logs an error with context.

    Args:
        context: Where the error occurred (e.g., 'chat_utils.generate_response').
        error_message: A descriptive error message.
        exception: The exception object (optional).
    """
    logger.bind(
        event_type="error",
        context=context
    ).error(f"Error in {context}: {error_message}")

    if exception:
        logger.exception(exception)

def log_user_action(user_id: str, action: str, details: dict = None):
    """
    Logs a user action.

    Args:
        user_id: The ID of the user.
        action: The action performed (e.g., 'send_message', 'clear_history').
        details: Additional details about the action.
    """
    logger.bind(
        event_type="user_action",
        user_id=user_id,
        action=action,
        details=details or {}
    ).info(f"User {user_id} performed {action}")

def log_system_event(event_name: str, details: dict = None):
    """
    Logs a system level event.

    Args:
        event_name: Name of the event (e.g., 'startup', 'shutdown').
        details: Additional details.
    """
    logger.bind(
        event_type="system_event",
        event_name=event_name,
        details=details or {}
    ).info(f"System Event: {event_name}")

if __name__ == "__main__":
    # Smoke test
    configure_logging()
    log_system_event("analytics_test_run")
    print("Analytics module test run complete.")
