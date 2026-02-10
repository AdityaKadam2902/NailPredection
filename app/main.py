from flask import Flask, send_from_directory, request, jsonify, render_template
from flask_cors import CORS
import os
import logging
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from werkzeug.utils import secure_filename

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'template')

app = Flask(__name__, static_folder=None, template_folder=TEMPLATE_DIR)
CORS(app)

# Upload and model config
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXT = {'.jpg', '.jpeg', '.png', '.bmp'}

# Try multiple model locations (static/models/... or project root)
MODEL_FILENAME = 'vgg-16-nail-disease.h5'
MODEL_PATHS = [
    os.path.join(BASE_DIR, 'static', 'models', MODEL_FILENAME),
    os.path.join(BASE_DIR, MODEL_FILENAME),
]

model = None
for p in MODEL_PATHS:
    if os.path.exists(p):
        try:
            logger.info(f'Loading model from: {p}')
            model = load_model(p)
            logger.info(f'Model loaded. Input shape: {getattr(model, "input_shape", None)}; output shape: {getattr(model, "output_shape", None)}')
            break
        except Exception as e:
            logger.exception(f'Failed loading model at {p}: {e}')
if model is None:
    logger.error('Model file not found in expected locations: %s', MODEL_PATHS)
    # Continue running — /predict will return an error if model is missing.

# Class labels (keep ordering consistent with training)
class_labels = [
    "Darier's disease",
    "Muehrcke's lines",
    "Alopecia areata",
    "Beau's lines",
    "Bluish nail",
    "Clubbing",
    "Eczema",
    "Half and half nails (Lindsay's nails)",
    "Koilonychia",
    "Leukonychia",
    "Onycholysis",
    "Pale nail",
    "Red lunula",
    "Splinter hemorrhage",
    "Terry's nail",
    "White nail",
    "Yellow nails"
]

# Serve the static HTML and assets
ALLOWED_STATIC = {
    'index.html', 'about.html', 'nailhome.html', 'nailpred.html',
    'main.css', 'main.js', 'styles.css', 'script.js'
}

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/nailhome.html')
def nailhome():
    return render_template('nailhome.html')

@app.route('/nailpred.html')
def nailpred():
    return render_template('nailpred.html')

@app.route('/<path:filename>')
def serve_file(filename):
    # serve only allowed files to avoid exposing the whole FS
    if filename in ALLOWED_STATIC:
        return send_from_directory(BASE_DIR, filename)
    # allow serving files under static/ (images, uploads, models) if requested
    if filename.startswith('static/'):
        rel = filename[len('static/'):]
        return send_from_directory(os.path.join(BASE_DIR, 'static'), rel)
    return jsonify({'error': 'Not found'}), 404

def allowed_file(filename):
    _, ext = os.path.splitext(filename.lower())
    return ext in ALLOWED_EXT

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        logger.error('Prediction requested but model is not loaded.')
        return jsonify({'error': 'Model not available on server'}), 500

    if 'file' not in request.files:
        logger.warning('No file part in request')
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if not file or file.filename == '':
        logger.warning('Empty filename received')
        return jsonify({'error': 'No file selected'}), 400

    filename = secure_filename(file.filename)
    if not allowed_file(filename):
        logger.warning('Disallowed file extension: %s', filename)
        return jsonify({'error': 'Unsupported file type'}), 400

    save_path = os.path.join(UPLOAD_FOLDER, filename)
    try:
        file.save(save_path)
        logger.info('Saved uploaded file to %s', save_path)
    except Exception as e:
        logger.exception('Failed saving uploaded file: %s', e)
        return jsonify({'error': 'Failed to save uploaded file'}), 500

    # Preprocess image for model
    try:
        img = image.load_img(save_path, target_size=(224, 224))
        arr = image.img_to_array(img) / 255.0
        arr = np.expand_dims(arr, axis=0)
        logger.info('Image preprocessed, shape=%s', arr.shape)
    except Exception as e:
        logger.exception('Image processing error: %s', e)
        return jsonify({'error': 'Image processing failed'}), 400

    # Check model output compatibility
    try:
        out_shape = model.output_shape
        if len(out_shape) < 2 or out_shape[1] != len(class_labels):
            logger.error('Model output shape mismatch: %s vs %s', out_shape, len(class_labels))
            return jsonify({'error': 'Model output shape does not match label count'}), 500
    except Exception as e:
        logger.exception('Unable to verify model output: %s', e)
        return jsonify({'error': 'Server model configuration error'}), 500

    # Predict
    try:
        preds = model.predict(arr)
        idx = int(np.argmax(preds[0]))
        label = class_labels[idx]
        confidence = float(preds[0][idx])
        logger.info('Prediction: %s (%.4f)', label, confidence)
        return jsonify({'disease_name': label, 'confidence': round(confidence * 100, 2)})
    except Exception as e:
        logger.exception('Prediction failed: %s', e)
        return jsonify({'error': 'Prediction failed'}), 500

if __name__ == '__main__':
    # Bind to 0.0.0.0 for network access; change host/port as needed
    app.run(host='0.0.0.0', port=5000, debug=True)