"""NailCareAI Configuration Management."""

import os


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "nailcare-ai-dev-key")
    DEBUG = False
    TESTING = False
    MAX_CONTENT_LENGTH = int(os.environ.get("MAX_UPLOAD_SIZE_MB", "10")) * 1024 * 1024
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "frontend", "static", "uploads")
    ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
    MODEL_FILENAME = os.environ.get("MODEL_FILENAME", "vgg-16-nail-disease.h5")
    MODEL_INPUT_SIZE = (224, 224)
    MODEL_NORMALIZATION = 255.0
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*").split(",")
    RATE_LIMIT_DEFAULT = os.environ.get("RATE_LIMIT_DEFAULT", "100 per hour")
    RATE_LIMIT_PREDICT = os.environ.get("RATE_LIMIT_PREDICT", "30 per minute")
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
    APP_NAME = "NailCareAI"
    APP_VERSION = "1.0.0"
    APP_DESCRIPTION = "AI-powered nail disease screening system"


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    LOG_LEVEL = "DEBUG"


class TestingConfig(BaseConfig):
    TESTING = True
    DEBUG = True


class ProductionConfig(BaseConfig):
    SECRET_KEY = os.environ.get("SECRET_KEY", "")
    DEBUG = False


_CONFIG_MAP = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def get_config(config_name):
    config_name = config_name.lower()
    if config_name not in _CONFIG_MAP:
        raise ValueError(f"Unknown config '{config_name}'")
    return _CONFIG_MAP[config_name]
