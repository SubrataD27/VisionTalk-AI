from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
import torch
from PIL import Image

class ImageCaptioner:
    def __init__(self):
        """Initialize the image captioning model"""
        self.model = VisionEncoderDecoderModel.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        self.feature_extractor = ViTImageProcessor.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        self.tokenizer = AutoTokenizer.from_pretrained("nlpconnect/vit-gpt2-image-captioning")
        
        # Set device to GPU if available, else CPU
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        
        # Set generation parameters
        self.model.config.decoder_start_token_id = self.tokenizer.cls_token_id
        self.model.config.pad_token_id = self.tokenizer.pad_token_id
        
    def generate_caption(self, image_path):
        """Generate a caption for the given image"""
        try:
            # Open image
            image = Image.open(image_path).convert('RGB')
            
            # Process image
            pixel_values = self.feature_extractor(images=[image], return_tensors="pt").pixel_values
            pixel_values = pixel_values.to(self.device)
            
            # Generate caption
            output_ids = self.model.generate(pixel_values, max_length=50)
            
            # Decode the caption
            caption = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
            
            return {
                "success": True,
                "caption": caption
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }