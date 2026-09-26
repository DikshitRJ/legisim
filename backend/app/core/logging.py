"""Structured Logging Configuration.

Provides JSON-formatted logging for production environments and human-readable
logging for development environments using Python's standard logging module.
"""

from __future__ import annotations

import json
import logging
import sys
from datetime import UTC, datetime
from typing import Any

from app.config import settings


class JSONFormatter(logging.Formatter):
    """Custom logging formatter that outputs log records as structured JSON."""

    def format(self, record: logging.LogRecord) -> str:
        """Format a LogRecord into a JSON string.

        Args:
            record: The LogRecord instance to format.

        Returns:
            str: JSON-encoded log line.
        """
        log_entry: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "environment": settings.ENVIRONMENT,
        }

        # Include exception traceback if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)

        # Include any custom extra keys passed to logger calls
        standard_attrs = {
            "name",
            "msg",
            "args",
            "levelname",
            "levelno",
            "pathname",
            "filename",
            "module",
            "exc_info",
            "exc_text",
            "stack_info",
            "lineno",
            "funcName",
            "created",
            "msecs",
            "relativeCreated",
            "thread",
            "threadName",
            "processName",
            "process",
            "message",
        }
        extras = {k: v for k, v in record.__dict__.items() if k not in standard_attrs}
        if extras:
            log_entry["extra"] = extras

        return json.dumps(log_entry, default=str)


def setup_logging(log_level: int = logging.INFO) -> None:
    """Configure root and application loggers based on current environment.

    In production, logs are formatted as JSON lines.
    In development, human-readable colored or formatted text is emitted.

    Args:
        log_level: Base logging level to apply.
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Clear existing handlers to prevent duplicate lines
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)

    if settings.ENVIRONMENT == "production":
        console_handler.setFormatter(JSONFormatter())
    else:
        dev_format = (
            "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s"
        )
        console_handler.setFormatter(logging.Formatter(dev_format, datefmt="%Y-%m-%d %H:%M:%S"))

    root_logger.addHandler(console_handler)

    # Adjust external noisy libraries
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
    if settings.ENVIRONMENT == "production":
        logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    else:
        logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)


def get_logger(name: str) -> logging.Logger:
    """Obtain a namespaced logger instance.

    Args:
        name: Name of the logger, typically __name__.

    Returns:
        logging.Logger: Configured logger instance.
    """
    return logging.getLogger(name)
