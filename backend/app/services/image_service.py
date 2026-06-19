"""NailCareAI Image Service."""

import os
import logging
from typing import Tuple
from pathlib import Path

import numpy as np
from PIL import Image
from werkzeug.utils import secure_filename
from flask import current_app

from app.core.exceptions import FileValidationError, ImageProcessingError

logger = logging.getLogger(__name__)

IMAGE_MAGIC = {
    b"\xff\xd8\xff": "jpeg", b"\x89PNG": "png", b"BM": "bmp", b"RIFF": "webp"
}
MAX_DIMENSION = 4096


class ImageService:
    def __init__(self):
        self.allowed_extensions = current_app.config.get("ALLOWED_EXTENSIONS", {".jpg", ".jpeg", ".png", ".bmp", ".webp"})
        self.target_size = current_app.config.get("MODEL_INPUT_SIZE", (224, 224))
        self.normalization = current_app.config.get("MODEL_NORMALIZATION", 255.0)

    def validate_file(self, file_storage) -> Tuple[bool, str]:
        if not file_storage or not file_storage.filename:
            return False, "No file selected"
        filename = secure_filename(file_storage.filename)
        _, ext = os.path.splitext(filename.lower())
        if ext not in self.allowed_extensions:
            return False, f"Unsupported file type: {ext}"
        file_storage.seek(0, os.SEEK_END)
        file_size = file_storage.tell()
        file_storage.seek(0)
        max_size = current_app.config.get("MAX_CONTENT_LENGTH", 10 * 1024 * 1024)
        if file_size > max_size:
            return False, f"File too large. Max: {max_size / (1024*1024):.1f} MB"
        if file_size == 0:
            return False, "File is empty"
        return True, ""

    def validate_image_content(self, file_path: str) -> Tuple[bool, str, dict]:
        with open(file_path, "rb") as f:
            header = f.read(16)
        detected = None
        for magic, fmt in IMAGE_MAGIC.items():
            if header.startswith(magic):
                detected = fmt
                break
        if detected is None:
            return False, "Invalid image format", {}
        try:
            with Image.open(file_path) as img:
                img.verify()
        except Exception as e:
            return False, f"Corrupted image: {str(e)}", {}
        try:
            with Image.open(file_path) as img:
                w, h = img.size
                if w > MAX_DIMENSION or h > MAX_DIMENSION:
                    return False, f"Image too large ({w}x{h})", {}
                return True, "", {"width": w, "height": h, "format": img.format, "mode": img.mode}
        except Exception as e:
            return False, f"Cannot read metadata: {str(e)}", {}

    def preprocess(self, file_path: str) -> np.ndarray:
        try:
            with Image.open(file_path) as img:
                if img.mode != "RGB":
                    img = img.convert("RGB")
                img = img.resize(self.target_size, Image.Resampling.LANCZOS)
                arr = np.array(img, dtype=np.float32) / self.normalization
                return np.expand_dims(arr, axis=0)
        except Exception as e:
            raise ImageProcessingError(f"Preprocessing failed: {str(e)}")

    def save_upload(self, file_storage, upload_folder: str) -> str:
        filename = secure_filename(file_storage.filename)
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        name, ext = os.path.splitext(filename)
        unique = f"{name}_{timestamp}{ext}"
        save_path = os.path.join(upload_folder, unique)
        try:
            file_storage.save(save_path)
            return save_path
        except Exception as e:
            raise FileValidationError(f"Failed to save file: {str(e)}")


def get_image_service():
    return ImageService()
