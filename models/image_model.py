import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
from PIL import Image

class ImageAnalyzer:
    def __init__(self):
        """Initialize the image recognition model"""
        # Load the pre-trained ResNet50 model
        self.model = ResNet50(weights='imagenet')
        
    def analyze_image(self, img_path):
        """Analyze the image and return descriptions"""
        try:
            # Load and preprocess the image
            img = image.load_img(img_path, target_size=(224, 224))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)
            
            # Make prediction
            predictions = self.model.predict(x)
            results = decode_predictions(predictions, top=5)[0]
            
            # Format and return the results
            descriptions = []
            for _, label, score in results:
                descriptions.append({
                    "label": label.replace("_", " ").title(),
                    "confidence": float(score) * 100
                })
            
            return {
                "success": True,
                "descriptions": descriptions,
                "summary": f"This appears to be a {descriptions[0]['label']} with {descriptions[0]['confidence']:.2f}% confidence."
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }