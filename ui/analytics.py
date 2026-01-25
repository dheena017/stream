import sys
import json
import datetime
from pathlib import Path
from loguru import logger
from typing import List, Dict, Any, Optional

# Ensure logs directory exists
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"

def init_analytics():
    """Initialize logging configuration."""
    logger.remove()

    # JSON Sink for machine parsing
    logger.add(
        LOG_FILE,
        rotation="10 MB",
        retention="10 days",
        level="INFO",
        serialize=True
    )

    # Console Sink for human reading (standard format)
    logger.add(
        sys.stderr,
        level="INFO",
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>"
    )

def log_api_call(provider: str, model: str, duration: float, success: bool, error_msg: Optional[str] = None):
    """Log an API call event."""
    log = logger.bind(
        event_type="api_call",
        provider=provider,
        model=model,
        duration=duration,
        success=success,
        error_details=error_msg
    )
    msg = f"API Call: {provider} - {model} ({'Success' if success else 'Failed'})"
    if success:
        log.info(msg)
    else:
        log.error(msg)

def log_error(context: str, error: Exception):
    """Log an application error."""
    logger.bind(event_type="error", context=context).exception(f"Error in {context}: {str(error)}")

def log_session(username: str, action: str):
    """Log a user session event."""
    logger.bind(event_type="session", username=username).info(f"Session: {username} - {action}")

def get_recent_errors(limit: int = 10) -> List[Dict[str, Any]]:
    """Retrieve recent error logs."""
    errors = []
    if not LOG_FILE.exists():
        return errors

    try:
        lines = []
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line in reversed(lines):
            try:
                record = json.loads(line)
                rec = record.get('record', {})
                if rec.get('level', {}).get('name') == "ERROR":
                    # Try to convert timestamp to readable
                    try:
                        ts = rec.get('time', {}).get('timestamp', 0)
                        readable_time = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                    except:
                        readable_time = rec.get('time', {}).get('repr', '')

                    msg = rec.get('message', 'Unknown Error')
                    extra = rec.get('extra', {})
                    exc = rec.get('exception')

                    errors.append({
                        "time": readable_time,
                        "message": msg,
                        "context": extra.get('context', 'General'),
                        "exception": exc,
                        "error_details": extra.get('error_details')
                    })

                    if len(errors) >= limit:
                        break
            except json.JSONDecodeError:
                continue

    except Exception as e:
        print(f"Error reading logs: {e}", file=sys.stderr)

    return errors

def get_analytics_summary() -> Dict[str, Any]:
    """Get basic stats from current log file."""
    stats = {
        "total_errors": 0,
        "api_calls": 0,
        "successful_calls": 0,
        "failed_calls": 0,
        "providers": {}
    }

    if not LOG_FILE.exists():
        return stats

    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = json.loads(line)
                    record = data.get('record', {})
                    level = record.get('level', {}).get('name')
                    extra = record.get('extra', {})

                    if level == "ERROR":
                        stats["total_errors"] += 1

                    if extra.get('event_type') == "api_call":
                        stats["api_calls"] += 1
                        if extra.get('success'):
                            stats["successful_calls"] += 1
                        else:
                            stats["failed_calls"] += 1

                        prov = extra.get('provider', 'unknown')
                        stats["providers"][prov] = stats["providers"].get(prov, 0) + 1

                except Exception:
                    continue
    except Exception:
        pass

    return stats
