"""Centralized logging configuration for the bot."""
import logging
import os
import sys
from logging.handlers import RotatingFileHandler


def configure_logging() -> None:
    """Configure root logger with console and rotating file handlers.

    Honors environment variables:
    - LOG_LEVEL (default: INFO)
    - LOG_DIR (default: logs)
    """
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, log_level, logging.INFO)

    log_dir = os.getenv("LOG_DIR", "logs")
    try:
        os.makedirs(log_dir, exist_ok=True)
    except Exception:
        # best-effort: if directory creation fails, continue and let file handler fail later
        pass

    fmt = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"
    formatter = logging.Formatter(fmt, datefmt=datefmt)

    root = logging.getLogger()
    # remove any existing handlers to avoid duplicate logs when reloading
    for h in list(root.handlers):
        root.removeHandler(h)

    root.setLevel(level)

    sh = logging.StreamHandler(sys.stderr)
    sh.setLevel(level)
    sh.setFormatter(formatter)
    root.addHandler(sh)

    logfile = os.path.join(log_dir, "bot.log")
    try:
        fh = RotatingFileHandler(logfile, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8")
        fh.setLevel(level)
        fh.setFormatter(formatter)
        root.addHandler(fh)
    except Exception:
        # if file handler can't be created (permissions, path issues), continue with console only
        root.warning("Could not create log file handler %s; continuing with console only", logfile)

    # Reduce verbosity for noisy third-party libraries
    logging.getLogger("apscheduler").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.INFO)
