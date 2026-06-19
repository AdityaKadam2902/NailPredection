"""Security Utilities."""

import uuid
from werkzeug.utils import secure_filename


def sanitize_filename(filename):
    safe = secure_filename(filename)
    safe = safe.replace("..", "").replace("/", "_").replace("\\", "_")
    if safe.startswith("."):
        safe = "upload_" + safe
    if len(safe) > 100:
        name, ext = safe.rsplit(".", 1) if "." in safe else (safe, "")
        safe = name[:90] + (f".{ext}" if ext else "")
    return safe


def generate_request_id():
    return str(uuid.uuid4())
