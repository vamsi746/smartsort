import tensorflow as tf  # type: ignore
from tensorflow.keras.models import load_model  # type: ignore
from tensorflow.keras.applications import VGG16  # type: ignore
from tensorflow.keras.models import Sequential  # type: ignore
from tensorflow.keras.layers import Flatten, Dense, Dropout  # type: ignore
import os

def create_model():
    """Create the model architecture"""
    # Load base VGG16 model (without top layers)
    vgg = VGG16(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    vgg.trainable = False  # Freeze the base model

    # Build custom classifier on top
    model = Sequential([
        vgg,
        Flatten(),
        Dropout(0.5),
        Dense(128, activation='relu'),
        Dropout(0.3),
        Dense(28, activation='softmax')  # 28 classes
    ])
    
    return model

def load_model_safe(model_path):
    """Safely load the model with error handling"""
    try:
        # First try to load the model directly
        model = load_model(model_path, compile=False)
        print("✅ Model loaded successfully with direct loading.")
    except Exception as e:
        print(f"⚠️ Direct model loading failed: {e}")
        print("🔄 Creating model architecture and loading weights...")
        try:
            # Create the model architecture
            model = create_model()
            # Load the weights
            model.load_weights(model_path)
            print("✅ Model weights loaded successfully.")
        except Exception as e2:
            print(f"❌ Failed to load model weights: {e2}")
            raise Exception(f"Could not load model: {e} and {e2}")
    
    # Compile the model
    model.compile(
        optimizer='adam',
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model
