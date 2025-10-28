from flask import Flask, render_template, request, url_for
import os
from werkzeug.utils import secure_filename
import numpy as np
import requests
import gdown  # type: ignore
from model_utils import load_model_safe
# Import for image preprocessing - ignored for static analysis
from tensorflow.keras.preprocessing import image  # type: ignore

app = Flask(__name__)

# Ensure uploads folder exists
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 🔽 Google Drive model download setup
MODEL_PATH = "healthy_vs_rotten.h5"
MODEL_URL = "https://drive.google.com/uc?export=download&id=1-6P7R6fHLFA7N1qlx3xzmyyxFVd1fbch"

def download_model_from_gdrive(url, destination):
    """Download model file from Google Drive with proper handling"""
    print("📥 Downloading model from Google Drive using gdown...")
    try:
        # Use gdown for more reliable Google Drive downloads
        gdown.download(url, destination, quiet=False)
        print("✅ Model downloaded successfully with gdown.")
        return True
    except Exception as e:
        print(f"⚠️  gdown failed: {e}")
        print("🔄 Falling back to requests method...")
        
        # Fallback to requests method
        session = requests.Session()
        response = session.get(url, stream=True)
        
        # Check if we got a confirmation page instead of the file
        if b'confirm' in response.content:
            print("⚠️  Download requires confirmation, trying alternative method...")
            # Extract confirmation code and retry
            for key, value in response.cookies.items():
                if key.startswith('download_warning'):
                    confirm_token = value
                    break
            else:
                confirm_token = None
            
            # Reconstruct URL with confirmation token
            if confirm_token:
                url = url + "&confirm=" + confirm_token
                response = session.get(url, stream=True)
        
        # Save the file
        with open(destination, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        print("✅ Model downloaded successfully with fallback method.")
        return True

if not os.path.exists(MODEL_PATH):
    try:
        download_model_from_gdrive(MODEL_URL, MODEL_PATH)
    except Exception as e:
        print(f"❌ Failed to download model: {e}")
        raise

# Check if downloaded file is valid
if os.path.exists(MODEL_PATH):
    file_size = os.path.getsize(MODEL_PATH)
    print(f"📁 Model file size: {file_size} bytes")
    if file_size < 1000000:  # Less than 1MB, likely an error page
        print("⚠️  Model file seems too small, might be an error page")
        # Try to read first few bytes to check
        with open(MODEL_PATH, 'rb') as f:
            header = f.read(100)
            if b'html' in header.lower() or b'<html' in header.lower():
                print("❌ Downloaded file is an HTML page, not the model")
                os.remove(MODEL_PATH)  # Remove invalid file
                raise Exception("Model download failed - received HTML instead of file")

# 🔁 Load model with our safe loading utility
try:
    model = load_model_safe(MODEL_PATH)
    print("✅ Model loaded and compiled successfully.")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    raise

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

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return render_template("predict.html")

    if 'file' not in request.files:
        return "⚠️ No file part in the request"

    file = request.files['file']

    if file.filename == '':
        return "⚠️ No file selected"

    if file and file.filename:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Load and preprocess image
        try:
            # Use the directly imported image module
            img = image.load_img(filepath, target_size=(224, 224))
            img_array = image.img_to_array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            # Make prediction
            prediction = model.predict(img_array)[0]
            predicted_class = class_labels[np.argmax(prediction)]
            confidence = prediction[np.argmax(prediction)] * 100
            result = f"{predicted_class} ({confidence:.2f}%)"
        except Exception as e:
            return f"❌ Error during prediction: {str(e)}"

        return render_template("output.html", prediction=result, filename=filename)

    return "⚠️ Something went wrong"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route("/testbg")
def test_bg():
    return render_template("testbg.html")

# ✅ THIS STARTS THE FLASK SERVER
if __name__ == '__main__':
    app.run(debug=True)
