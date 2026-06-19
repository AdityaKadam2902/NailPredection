# NailCareAI

AI-powered nail disease screening system. Upload a nail image to detect 17 potential conditions using deep learning.

---

## Project Structure

```
nailcare-ai/
├── backend/                  # Flask API and business logic
│   ├── app/
│   │   ├── api/              # REST endpoints (routes.py)
│   │   ├── core/             # Constants, exceptions
│   │   ├── services/         # Model, image, prediction logic
│   │   ├── utils/            # Validation, security helpers
│   │   ├── config.py         # Environment configuration
│   │   ├── extensions.py     # CORS, rate limiting, logging
│   │   └── __init__.py       # App factory
│   ├── tests/                # pytest suite
│   └── run.py                # Entry point
│
├── frontend/                 # HTML, CSS, JS templates
│   ├── static/
│   │   ├── css/main.css      # Design system
│   │   └── js/main.js        # Upload, drag-drop, results
│   └── templates/            # Jinja2 HTML pages
│       ├── base.html
│       ├── index.html        # Landing page
│       ├── about.html        # Technology
│       ├── nailhome.html     # Disease library
│       └── nailpred.html     # Upload & results
│
├── data/                     # Dataset (train/test folders)
│   ├── train/                # Training images (17 class folders)
│   └── test/                 # Test images (17 class folders)
│
├── models/                   # Trained model storage
│   └── vgg-16-nail-disease.h5
│
├── scripts/                  # Training utilities
│   ├── rename_folders.py     # Fix dataset folder names
│   └── train.py              # Model training
│
├── requirements.txt          # Single requirements file
├── requirements-training.txt  # TensorFlow training-only dependencies
└── README.md                 # This file
```

---

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

If you want to train a real TensorFlow model, create a Python 3.12 virtual environment and install the training dependencies instead:

```powershell
python3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements-training.txt
```

### 2. Add Your Dataset

Place your nail disease images in the `data/` folder with this exact structure:

```
data/
├── train/
│   ├── Alopecia areata/
│   ├── Beau's lines/
│   ├── Bluish nail/
│   ├── Clubbing/
│   ├── Darier's disease/
│   ├── Eczema/
│   ├── Half and half nails (Lindsay's nails)/
│   ├── Koilonychia/
│   ├── Leukonychia/
│   ├── Muehrcke's lines/
│   ├── Onycholysis/
│   ├── Pale nail/
│   ├── Red lunula/
│   ├── Splinter hemorrhage/
│   ├── Terry's nail/
│   ├── White nail/
│   └── Yellow nails/
└── test/
    ├── (same 17 folders)
```

**Important:** Folder names must match exactly (case-sensitive, with apostrophes).

If your folder names have typos or underscores, run:

```bash
python scripts/rename_folders.py
```

### 3. Run the Application

```bash
cd backend
python run.py
```

Open browser: **http://localhost:5000**

---

## Training a Real Model

The app runs in **mock mode** by default (random predictions for demo). To train a real model:

### Requirements for Training
- **Python 3.12** (TensorFlow does not support Python 3.14)
- TensorFlow 2.16+

### Steps

```bash
# 1. Install Python 3.12 from https://www.python.org/downloads/

# 2. Create virtual environment with Python 3.12
python3.12 -m venv .venv

# 3. Activate
# Windows:
.venv\Scripts\Activate.ps1
# Mac/Linux:
source .venv/bin/activate

# 4. Install TensorFlow training dependencies
pip install -r requirements-training.txt

# 5. Train
python scripts/train.py --epochs 50 --batch-size 32

# 6. Move trained model to production
mkdir -p models
cp models/vgg-16-nail-disease.h5 models/

# 7. Run app
python backend/run.py
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Landing page |
| `/about.html` | GET | Technology page |
| `/nailhome.html` | GET | Disease library |
| `/nailpred.html` | GET | Upload page |
| `/api/health` | GET | Health check |
| `/api/version` | GET | App version |
| `/api/model-info` | GET | Model metadata |
| `/api/predict` | POST | Upload image, get prediction |
| `/predict` | POST | Legacy endpoint |

### Prediction Response

```json
{
  "success": true,
  "data": {
    "prediction": {
      "disease_name": "Terry's nail",
      "confidence": 94.23,
      "confidence_level": "High",
      "class_index": 14
    },
    "disease_info": {
      "description": "Mostly white with pink tip...",
      "symptoms": ["White nail", "Pink distal band"],
      "severity": "High",
      "next_steps": "Liver function tests..."
    },
    "top_predictions": [
      {"rank": 1, "disease_name": "Terry's nail", "confidence": 94.23},
      {"rank": 2, "disease_name": "White nail", "confidence": 3.12}
    ],
    "disclaimer": "This AI screening tool is for informational purposes only..."
  },
  "meta": {
    "timestamp": "2024-01-15T10:30:00",
    "processing_time_ms": 245.6,
    "model_version": "1.0.0"
  }
}
```

---

## 17 Detectable Conditions

1. Darier's disease
2. Muehrcke's lines
3. Alopecia areata
4. Beau's lines
5. Bluish nail
6. Clubbing
7. Eczema
8. Half and half nails (Lindsay's nails)
9. Koilonychia
10. Leukonychia
11. Onycholysis
12. Pale nail
13. Red lunula
14. Splinter hemorrhage
15. Terry's nail
16. White nail
17. Yellow nails

---

## Environment Variables

Create a `.env` file in the project root:

```env
FLASK_ENV=development
SECRET_KEY=your-secret-key
MAX_UPLOAD_SIZE_MB=10
CORS_ORIGINS=http://localhost:5000
MODEL_FILENAME=vgg-16-nail-disease.h5
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `TensorFlow not found` | Expected on Python 3.14. Use Python 3.12 for training. App runs in mock mode. |
| `pip install tensorflow` fails on Python 3.14 | Use a Python 3.12 venv and `requirements-training.txt` |
| `Folder names wrong` | Run `python scripts/rename_folders.py` |
| `Model not loading` | Ensure `models/vgg-16-nail-disease.h5` exists. App falls back to mock mode. |
| `File too large` | Increase `MAX_UPLOAD_SIZE_MB` in `.env` |
| `CORS error` | Add your domain to `CORS_ORIGINS` in `.env` |

---

## Medical Disclaimer

This AI screening tool is for **informational and educational purposes only**. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of a qualified healthcare provider with any questions regarding a medical condition.

---


