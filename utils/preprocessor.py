import cv2
import numpy as np
import os

def preprocess_image(file_path, save_path=None):
    """Preprocess the image for better recognition"""
    # Read the image
    image = cv2.imread(file_path)
    
    # Convert to RGB (OpenCV uses BGR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Resize the image to a standard size
    image = cv2.resize(image, (224, 224))
    
    # Normalize the image
    image = image / 255.0
    
    if save_path:
        # Convert back to BGR for saving
        save_image = cv2.cvtColor((image * 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
        cv2.imwrite(save_path, save_image)
    
    return image