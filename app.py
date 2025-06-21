from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import requests

app = Flask(__name__)

# Ensure uploads folder exists
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 🔽 Google Drive model download setup
MODEL_PATH = "healthy_vs_rotten.h5"
MODEL_URL = "https://drive.google.com/uc?export=download&id=1-6P7R6fHLFA7N1qlx3xzmyyxFVd1fbch"

if not os.path.exists(MODEL_PATH):
    print("📥 Downloading model from Google Drive...")
    response = requests.get(MODEL_URL)
    with open(MODEL_PATH, "wb") as f:
        f.write(response.content)
    print("✅ Model downloaded successfully.")

# 🔁 Load model
model = load_model(MODEL_PATH)

# 🍎 Class labels
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

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

# ✅ THIS STARTS THE FLASK SERVER
if __name__ == '__main__':
    app.run(debug=True)
