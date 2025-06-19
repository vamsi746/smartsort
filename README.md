# 🥦 SmartSort - AI Powered Produce Classifier 🍎

**SmartSort** is an AI-powered web application that detects whether fruits and vegetables are *fresh* or *rotten* using deep learning (VGG16). Built with a modern UI and deployed on Render, this tool provides instant quality analysis with a single image upload.

---

## 🚀 Live Demo

🔗 **[SmartSort Live App](https://smartsort-backend.onrender.com)**

---

## 📸 Screenshots

### 🏠 Home Page  
![Home](https://raw.githubusercontent.com/vamsi746/smartsort/main/static/img/home.png.PNG)

### 🔍 Predict Page  
![Predict](https://raw.githubusercontent.com/vamsi746/smartsort/main/static/img/predict.png.PNG)

### 📈 Result Output  
![Result](https://raw.githubusercontent.com/vamsi746/smartsort/main/static/img/result.png.PNG)


## 💡 Features

- ✅ Upload an image of a fruit or vegetable  
- ✅ Predict whether it’s **Healthy** or **Rotten**  
- ✅ Stunning modern UI with dark theme and glassmorphism  
- ✅ Fully responsive for all devices  
- ✅ Backend powered by Flask + TensorFlow (VGG16)  
- ✅ Hosted & Live on Render

---

## ⚙️ Technologies Used

- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Python Flask  
- **Deep Learning:** TensorFlow, Keras, VGG16  
- **Deployment:** Render (Backend), GitHub Hosting  

---

## 📦 How to Run Locally

```bash
# Clone the repository
git clone https://github.com/vamsi746/smartsort.git
cd smartsort

# Optional: create virtual environment
python -m venv venv
venv\Scripts\activate     # For Windows
# source venv/bin/activate  # For macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the Flask application
python app.py
📁 Project Structure
app.py — Flask backend

healthy_vs_rotten.h5 — Trained model

templates/ — HTML pages (index.html, predict.html, output.html, etc.)

static/css/style.css — Styling

static/img/ — Icons, banners, and background images

requirements.txt — Python packages

render.yaml, Dockerfile, runtime.txt — Deployment configs

🙌 Acknowledgements
🍏 Dataset: Fruit and Vegetable Diseases Dataset (Kaggle)

🧠 Transfer Learning: VGG16 model

🌐 UI Inspired by NutriGaze

🚀 Hosted using Render

✍️ Author
🔥 VAMSI 🔥
💼 LinkedIn: https://www.linkedin.com/in/lakshmi-narayana-sangaraju-a814472b6/
🐙 GitHub: https://github.com/vamsi746

💡 Passionate Web Developer | AI Enthusiast | Builder of Cool Projects

📄 License
This project is licensed under the MIT License - feel free to use and modify!

