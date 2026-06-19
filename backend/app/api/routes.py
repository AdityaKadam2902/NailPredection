"""NailCareAI API Routes."""

from flask import Blueprint, request, jsonify, render_template, send_from_directory, current_app
from datetime import datetime, timezone
import os
import logging

from app.services.prediction_service import get_prediction_service
from app.core.exceptions import NailCareAIError, FileValidationError, ValidationError

logger = logging.getLogger(__name__)
api_bp = Blueprint("api", __name__)


def _add_meta(response):
    if "meta" not in response:
        response["meta"] = {}
    response["meta"]["timestamp"] = datetime.now(timezone.utc).isoformat()
    return response


@api_bp.route("/")
def index():
    return render_template("index.html")

@api_bp.route("/index.html")
def index_html():
    return render_template("index.html")

@api_bp.route("/about.html")
def about():
    return render_template("about.html")

@api_bp.route("/nailhome.html")
def nailhome():
    return render_template("nailhome.html")

@api_bp.route("/nailpred.html")
def nailpred():
    return render_template("nailpred.html")

@api_bp.route("/static/<path:filename>")
def serve_static(filename):
    static_dir = os.path.join(current_app.root_path, "..", "..", "frontend", "static")
    return send_from_directory(static_dir, filename)


@api_bp.route("/api/health", methods=["GET"])
def health():
    try:
        service = get_prediction_service()
        return jsonify(_add_meta(service.get_health_status()))
    except Exception as e:
        return jsonify(_add_meta({"success": False, "data": {"status": "error"}})), 500


@api_bp.route("/api/version", methods=["GET"])
def version():
    return jsonify(_add_meta({
        "success": True,
        "data": {"name": current_app.config.get("APP_NAME"), "version": current_app.config.get("APP_VERSION")}
    }))


@api_bp.route("/api/model-info", methods=["GET"])
def model_info():
    try:
        service = get_prediction_service()
        return jsonify(_add_meta(service.get_model_info()))
    except Exception as e:
        return jsonify(_add_meta({"success": False, "error": {"code": "MODEL_INFO_ERROR", "message": str(e)}})), 500


@api_bp.route("/api/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify(_add_meta({"success": False, "error": {"code": "MISSING_FILE", "message": "No file uploaded"}})), 400

    file = request.files["file"]
    try:
        service = get_prediction_service()
        result = service.predict(file)
        return jsonify(_add_meta(result))
    except FileValidationError as e:
        return jsonify(_add_meta({"success": False, "error": {"code": e.error_code, "message": e.message}})), e.status_code
    except ValidationError as e:
        return jsonify(_add_meta({"success": False, "error": {"code": e.error_code, "message": e.message}})), e.status_code
    except NailCareAIError as e:
        return jsonify(_add_meta({"success": False, "error": {"code": e.error_code, "message": e.message}})), e.status_code
    except Exception as e:
        logger.exception("Prediction error: %s", e)
        return jsonify(_add_meta({"success": False, "error": {"code": "INTERNAL_ERROR", "message": "Prediction failed"}})), 500


@api_bp.route("/predict", methods=["POST"])
def predict_legacy():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files["file"]
    try:
        service = get_prediction_service()
        result = service.predict(file)
        pred = result["data"]["prediction"]
        return jsonify({"disease_name": pred["disease_name"], "confidence": pred["confidence"]})
    except Exception as e:
        return jsonify({"error": str(e) if hasattr(e, "message") else "Prediction failed"}), 500
