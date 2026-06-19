"""Validation Utilities."""

import os


def validate_file_extension(filename, allowed_extensions):
    if not filename:
        return False, "Filename is empty"
    _, ext = os.path.splitext(filename.lower())
    if ext not in allowed_extensions:
        return False, f"Unsupported file type: {ext}"
    return True, ""
