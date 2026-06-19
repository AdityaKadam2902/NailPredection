"""NailCareAI Prediction Service."""

import logging
import time
from typing import Dict, Any, List
from datetime import datetime, timezone

from app.core.constants import CLASS_LABELS, DISEASE_INFO, MEDICAL_DISCLAIMER
from app.core.exceptions import FileValidationError, ImageProcessingError, ModelNotLoadedError
from app.services.model_service import get_model_service
from app.services.image_service import get_image_service

logger = logging.getLogger(__name__)


class PredictionService:
    def __init__(self):
        self.model_service = get_model_service()
        self.image_service = get_image_service()

    def predict(self, file_storage) -> Dict[str, Any]:
        start = time.perf_counter()
        timestamp = datetime.now(timezone.utc).isoformat()

        is_valid, error = self.image_service.validate_file(file_storage)
        if not is_valid:
            raise FileValidationError(error)

        from flask import current_app
        upload_folder = current_app.config.get("UPLOAD_FOLDER")
        file_path = self.image_service.save_upload(file_storage, upload_folder)

        is_valid, error, metadata = self.image_service.validate_image_content(file_path)
        if not is_valid:
            import os
            try: os.remove(file_path)
            except: pass
            raise FileValidationError(error)

        image_array = self.image_service.preprocess(file_path)

        if not self.model_service.is_loaded:
            if not self.model_service.load():
                raise ModelNotLoadedError()

        class_idx, label, confidence, probabilities = self.model_service.predict(image_array)
        processing_time = round((time.perf_counter() - start) * 1000, 2)

        top_preds = self._build_top_k(probabilities)
        info = DISEASE_INFO.get(label, {})
        conf_pct = round(confidence * 100, 2)
        level = "High" if conf_pct >= 85 else "Moderate" if conf_pct >= 60 else "Low"

        return {
            "success": True,
            "data": {
                "prediction": {"disease_name": label, "confidence": conf_pct, "confidence_level": level, "class_index": class_idx},
                "disease_info": {"description": info.get("description", ""), "symptoms": info.get("symptoms", []), "severity": info.get("severity", "Unknown"), "next_steps": info.get("next_steps", "")},
                "top_predictions": top_preds,
                "image_metadata": metadata,
                "disclaimer": MEDICAL_DISCLAIMER,
            },
            "meta": {
                "timestamp": timestamp,
                "processing_time_ms": processing_time,
                "model_version": "1.0.0",
                "model_name": "VGG-16",
                "mock_mode": self.model_service.get_metadata().get("mock_mode", False),
            },
        }

    def _build_top_k(self, probabilities, k=5):
        indices = probabilities.argsort()[::-1][:k]
        labels = self.model_service.get_class_labels()
        return [{"rank": i+1, "disease_name": labels[idx], "confidence": round(float(probabilities[idx]) * 100, 2)} for i, idx in enumerate(indices)]

    def get_model_info(self):
        if not self.model_service.is_loaded:
            self.model_service.load()
        labels = self.model_service.get_class_labels()
        return {"success": True, "data": {"model": self.model_service.get_metadata(), "classes": labels, "num_classes": len(labels)}}

    def get_health_status(self):
        if not self.model_service.is_loaded:
            self.model_service.load()
        meta = self.model_service.get_metadata()
        status = "healthy" if self.model_service.is_loaded and not meta.get("mock_mode", False) else "degraded"
        return {
            "success": True,
            "data": {
                "status": status,
                "model": "healthy" if self.model_service.is_loaded and not meta.get("mock_mode", False) else "mock",
                "mock_mode": meta.get("mock_mode", False),
                "has_tensorflow": meta.get("has_tensorflow", False),
                "model_path": meta.get("model_path", ""),
            },
        }


def get_prediction_service():
    return PredictionService()
