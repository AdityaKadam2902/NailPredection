"""NailCareAI Model Service - with Mock Mode for Python 3.14+."""

import os
import logging
import random
import json
from typing import Optional, Dict, Any, Tuple

import numpy as np
from pathlib import Path

from app.core.constants import MODEL_METADATA, CLASS_LABELS, NUM_CLASSES
from app.core.exceptions import ModelNotLoadedError

logger = logging.getLogger(__name__)


class ModelService:
    _instance: Optional["ModelService"] = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, model_filename="vgg-16-nail-disease.h5", base_dir=None):
        if self._initialized:
            return
        self._model = None
        self._model_filename = model_filename
        self._base_dir = Path(base_dir) if base_dir else Path(__file__).resolve().parents[3]
        self._is_loaded = False
        self._mock_mode = False
        self._has_tf = False
        self._class_labels = CLASS_LABELS.copy()
        self._labels_source = "built-in defaults"

        try:
            from tensorflow.keras.models import load_model
            self._has_tf = True
        except ImportError:
            logger.warning("TensorFlow not available. Running in MOCK mode.")

        self._initialized = True

    @property
    def is_loaded(self):
        return self._is_loaded or self._mock_mode

    def load(self):
        if not self._has_tf:
            self._mock_mode = True
            self._is_loaded = True
            return True

        model_path = (self._base_dir / "models" / self._model_filename).resolve()
        if model_path.exists():
            try:
                from tensorflow.keras.models import load_model
                self._model = load_model(str(model_path))
                self._load_class_labels(model_path.parent)
                self._is_loaded = True
                self._mock_mode = False
                return True
            except Exception as e:
                logger.error("Failed to load model: %s", e)

        self._mock_mode = True
        self._is_loaded = True
        return True

    def _load_class_labels(self, models_dir: Path) -> None:
        labels_path = models_dir / "class_labels.json"
        if not labels_path.exists():
            self._class_labels = CLASS_LABELS.copy()
            self._labels_source = "built-in defaults"
            return

        try:
            with labels_path.open("r", encoding="utf-8") as f:
                labels = json.load(f)
            if isinstance(labels, list) and len(labels) == NUM_CLASSES:
                self._class_labels = labels
                self._labels_source = str(labels_path)
            else:
                logger.warning("Ignoring invalid class label file at %s", labels_path)
                self._class_labels = CLASS_LABELS.copy()
                self._labels_source = "built-in defaults"
        except Exception as e:
            logger.warning("Failed to load class labels from %s: %s", labels_path, e)
            self._class_labels = CLASS_LABELS.copy()
            self._labels_source = "built-in defaults"

    def get_metadata(self):
        meta = MODEL_METADATA.copy()
        meta.update({
            "loaded": self._is_loaded,
            "mock_mode": self._mock_mode,
            "has_tensorflow": self._has_tf,
            "model_path": str((self._base_dir / "models" / self._model_filename).resolve()),
            "labels_source": self._labels_source,
        })
        return meta

    def predict(self, image_array: np.ndarray):
        if not self._is_loaded:
            if not self.load():
                raise ModelNotLoadedError()

        if self._mock_mode:
            class_idx = random.randint(0, NUM_CLASSES - 1)
            confidence = random.uniform(0.70, 0.98)
            probabilities = np.random.dirichlet(np.ones(NUM_CLASSES) * 0.5)
            probabilities[class_idx] = confidence
            probabilities = probabilities / probabilities.sum()
            return class_idx, CLASS_LABELS[class_idx], float(confidence), probabilities

        predictions = self._model.predict(image_array, verbose=0)
        probabilities = predictions[0]
        class_idx = int(np.argmax(probabilities))
        return class_idx, self._class_labels[class_idx], float(probabilities[class_idx]), probabilities

    def get_class_labels(self):
        return self._class_labels.copy()


def get_model_service(model_filename=None, base_dir=None):
    if ModelService._instance is None or not ModelService._instance._initialized:
        ModelService._instance = ModelService(model_filename or "vgg-16-nail-disease.h5", base_dir)
    return ModelService._instance
