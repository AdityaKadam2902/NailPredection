"""NailCareAI Custom Exceptions and Error Handlers."""

from flask import Flask, jsonify, request
import logging

logger = logging.getLogger(__name__)


class NailCareAIError(Exception):
    def __init__(self, message, status_code=500, error_code="INTERNAL_ERROR"):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code


class ValidationError(NailCareAIError):
    def __init__(self, message, error_code="VALIDATION_ERROR"):
        super().__init__(message, status_code=400, error_code=error_code)


class FileValidationError(ValidationError):
    def __init__(self, message):
        super().__init__(message, error_code="FILE_VALIDATION_ERROR")


class ModelNotLoadedError(NailCareAIError):
    def __init__(self, message="Model not available"):
        super().__init__(message, status_code=503, error_code="MODEL_NOT_LOADED")


class PredictionError(NailCareAIError):
    def __init__(self, message):
        super().__init__(message, status_code=500, error_code="PREDICTION_ERROR")


class ImageProcessingError(NailCareAIError):
    def __init__(self, message):
        super().__init__(message, status_code=400, error_code="IMAGE_PROCESSING_ERROR")


def register_error_handlers(app: Flask):
    @app.errorhandler(NailCareAIError)
    def handle_custom(error):
        return jsonify({"success": False, "error": {"code": error.error_code, "message": error.message}}), error.status_code

    @app.errorhandler(404)
    def handle_404(error):
        return jsonify({"success": False, "error": {"code": "NOT_FOUND", "message": "Resource not found"}}), 404

    @app.errorhandler(413)
    def handle_413(error):
        return jsonify({"success": False, "error": {"code": "FILE_TOO_LARGE", "message": "File too large"}}), 413

    @app.errorhandler(429)
    def handle_429(error):
        return jsonify({"success": False, "error": {"code": "RATE_LIMIT", "message": "Rate limit exceeded"}}), 429

    @app.errorhandler(Exception)
    def handle_generic(error):
        logger.exception("Unexpected error: %s", error)
        message = str(error) if app.config.get("DEBUG") else "An unexpected error occurred"
        return jsonify({"success": False, "error": {"code": "INTERNAL_ERROR", "message": message}}), 500
