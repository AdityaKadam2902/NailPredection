#!/usr/bin/env python3
"""NailCareAI Entry Point."""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

config_name = os.environ.get("FLASK_ENV", "production")
app = create_app(config_name)

if __name__ == "__main__":
    debug = app.config.get("DEBUG", False)
    port = int(os.environ.get("PORT", 5000))
    host = os.environ.get("HOST", "0.0.0.0")
    app.run(host=host, port=port, debug=debug)
