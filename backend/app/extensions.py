"""NailCareAI Flask Extensions."""

import logging
import sys
from flask import Flask
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Create limiter instance at module level (v3+ pattern)
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100 per hour"],
    storage_uri="memory://",
)


def init_extensions(app: Flask) -> None:
    """Initialize Flask extensions."""
    _init_logging(app)
    _init_cors(app)
    _init_limiter(app)


def _init_logging(app):
    log_level = getattr(logging, app.config.get("LOG_LEVEL", "INFO"), logging.INFO)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    handler.setLevel(log_level)
    app.logger.setLevel(log_level)
    app.logger.addHandler(handler)


def _init_cors(app):
    origins = app.config.get("CORS_ORIGINS", ["*"])
    if origins == [""]:
        origins = []
    CORS(app, origins=origins, supports_credentials=True)


def _init_limiter(app):
    limiter.init_app(app)
    # Apply config overrides after init
    default_limit = app.config.get("RATE_LIMIT_DEFAULT", "100 per hour")
    if default_limit:
        limiter.default_limits = [default_limit]