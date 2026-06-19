"""NailCareAI Application Factory."""

from flask import Flask
from .config import get_config
from .extensions import init_extensions
from .api.routes import api_bp
from .core.exceptions import register_error_handlers


def create_app(config_name="production") -> Flask:
    """Create and configure Flask application."""
    app = Flask(__name__, template_folder="../../frontend/templates", static_folder="../../frontend/static")

    config = get_config(config_name)
    app.config.from_object(config)

    init_extensions(app)
    app.register_blueprint(api_bp)
    register_error_handlers(app)

    upload_folder = app.config.get("UPLOAD_FOLDER")
    if upload_folder:
        import os
        os.makedirs(upload_folder, exist_ok=True)

    return app
