import torch
from PIL import Image
from transformers import BlipProcessor, BlipForQuestionAnswering

class VisualQA:
    def __init__(self):
        """Initialize the visual question answering model"""
        try:
            # Load BLIP model for visual question answering
            self.processor = BlipProcessor.from_pretrained("Salesforce/blip-vqa-base")
            self.model = BlipForQuestionAnswering.from_pretrained("Salesforce/blip-vqa-base")
            
            # Set device to GPU if available, else CPU
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model.to(self.device)
            
            self.initialized = True
        except Exception as e:
            print(f"Error initializing VisualQA model: {e}")
            self.initialized = False
    
    def answer_question(self, image_path, question):
        """Answer a question about an image"""
        if not self.initialized:
            return {
                "success": False,
                "error": "Model failed to initialize"
            }
        
        try:
            # Open and process the image
            raw_image = Image.open(image_path).convert('RGB')
            
            # Prepare inputs for the model
            inputs = self.processor(raw_image, question, return_tensors="pt").to(self.device)
            
            # Generate answer
            with torch.no_grad():
                outputs = self.model.generate(**inputs)
                answer = self.processor.decode(outputs[0], skip_special_tokens=True)
            
            return {
                "success": True,
                "answer": answer
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def is_available(self):
        """Check if the model is available"""
        return self.initialized