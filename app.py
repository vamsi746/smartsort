from flask import Flask, render_template, request
import os
import requests
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np

app = Flask(__name__)

# Ensure uploads folder exists
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ✅ Step: Download model if not present
model_url = 'https://drive.google.com/uc?export=download&id=1-6P7R6fHLFA7N1qlx3xzmyyxFVd1fbch'
model_path = 'healthy_vs_rotten.h5'

if not os.path.exists(model_path):
    print("📦 Downloading model...")
    r = requests.get(model_url)
    with open(model_path, 'wb') as f:
        f.write(r.content)
    print("✅ Model downloaded!")

# ✅ Load model
model = load_model(model_path)

class_labels = [
    'Apple__Healthy', 'Apple__Rotten', 'Banana__Healthy', 'Banana__Rotten',
    'Bellpepper__Healthy', 'Bellpepper__Rotten', 'Carrot__Healthy', 'Carrot__Rotten',
    'Cucumber__Healthy', 'Cucumber__Rotten', 'Grape__Healthy', 'Grape__Rotten',
    'Guava__Healthy', 'Guava__Rotten', 'Jujube__Healthy', 'Jujube__Rotten',
    'Mango__Healthy', 'Mango__Rotten', 'Orange__Healthy', 'Orange__Rotten',
    'Pomegranate__Healthy', 'Pomegranate__Rotten', 'Potato__Healthy', 'Potato__Rotten',
    'Strawberry__Healthy', 'Strawberry__Rotten', 'Tomato__Healthy', 'Tomato__Rotten'
]

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return render_template("predict.html")

    if 'file' not in request.files:
        return "⚠️ No file part in the request"

    file = request.files['file']
    if file.filename == '':
        return "⚠️ No file selected"

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Load and preprocess image
        img = image.load_img(filepath, target_size=(224, 224))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        prediction = model.predict(img_array)[0]
        predicted_class = class_labels[np.argmax(prediction)]
        confidence = prediction[np.argmax(prediction)] * 100
        result = f"{predicted_class} ({confidence:.2f}%)"

        return render_template("output.html", prediction=result, filename=filename)

    return "⚠️ Something went wrong"
