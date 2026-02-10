NailCareAI 💅🤖

Early-Stage Nail Disease Detection Using Deep Learning

NailCareAI is a web-based deep learning application that detects potential nail diseases from nail images. The system uses a pre-trained VGG16-based CNN model and provides predictions through a simple, user-friendly interface.

This project aims to assist early diagnosis and reduce the workload on medical professionals by providing AI-based preliminary analysis.

🚀 Features

Upload nail images for disease prediction

Deep learning model trained using transfer learning

Supports 17 different nail disease classes

Web-based interface (HTML + CSS + JS)

REST API for prediction using Flask

Confidence score returned with predictions

🧠 Diseases Supported

The model can detect the following nail conditions:

Darier's disease

Muehrcke's lines

Alopecia areata

Beau's lines

Bluish nail

Clubbing

Eczema

Half and half nails (Lindsay's nails)

Koilonychia

Leukonychia

Onycholysis

Pale nail

Red lunula

Splinter hemorrhage

Terry's nail

White nail

Yellow nails

🏗️ Tech Stack
Backend

Python

Flask

Flask-CORS

TensorFlow / Keras

NumPy

Frontend

HTML5

CSS3

JavaScript

Deep Learning

VGG16 (Transfer Learning)

Image input size: 224 x 224

⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/your-username/NailCareAI.git
cd NailCareAI

2️⃣ Create Virtual Environment (Recommended)
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

3️⃣ Install Dependencies
pip install flask flask-cors tensorflow numpy pillow

4️⃣ Add Model File

Place the trained model file at either:

static/models/vgg-16-nail-disease.h5


or in the project root directory.

▶️ Run the Application
python main.py


Server will start at:

http://127.0.0.1:5000

🌐 Web Pages
Page	URL
Home	/index.html
About	/about.html
Nail Info	/nailhome.html
Prediction	/nailpred.html
🔌 API Endpoint
POST /predict

Request

Content-Type: multipart/form-data

Field name: file

Response

{
  "disease_name": "Koilonychia",
  "confidence": 92.45
}

🛡️ Validations & Security

Only image files allowed (.jpg, .jpeg, .png, .bmp)

Secure file upload handling

Model output validation

Error handling for missing model or invalid input

⚠️ Disclaimer

This system is not a medical diagnostic tool.
Predictions are for educational and research purposes only and should not replace professional medical advice.

📌 Future Enhancements

Multiple model comparison (ResNet, Inception, Xception)

Mobile responsiveness

Doctor recommendation system

Cloud deployment

Patient history tracking

👨‍💻 Author

Aditya Kadam
B.Tech CSE
Project: AI-Based Nail Disease Detection System
