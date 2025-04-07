from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class ChatModel:
    def __init__(self):
        """Initialize the conversational model"""
        # Using DialoGPT-medium for better responses
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
        self.model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
        
        # Store conversation history
        self.chat_history_ids = None
        self.image_context = None
        
    def get_response(self, user_input):
        """Generate a response based on user input"""
        try:
            # Encode the user input
            inputs = self.tokenizer.encode(user_input + self.tokenizer.eos_token, return_tensors='pt')
            
            # Append to chat history if it exists
            if self.chat_history_ids is not None:
                inputs = torch.cat([self.chat_history_ids, inputs], dim=-1)
            
            # Generate a response with improved parameters
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=2000,  # Increased max length for more detailed responses
                    pad_token_id=self.tokenizer.eos_token_id,
                    do_sample=True,
                    top_p=0.92,
                    top_k=50,
                    temperature=0.85,  # Slightly lowered temperature for more focused responses
                    repetition_penalty=1.2  # Helps avoid repetitive text
                )
            
            # Update chat history
            self.chat_history_ids = outputs
            
            # Decode the response
            response = self.tokenizer.decode(outputs[:, inputs.shape[-1]:][0], skip_special_tokens=True)
            
            # Handle empty responses
            if not response.strip():
                response = "I'm not sure how to respond to that question about this image. Could you try asking something else?"
            
            return {
                "success": True,
                "response": response
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def set_image_context(self, context):
        """Set the image context for better image-related responses"""
        self.image_context = context
        
    def get_response_with_image_context(self, question):
        """Get a response with the current image context"""
        if not self.image_context:
            return {
                "success": False,
                "error": "No image context available"
            }
            
        # Format the input with image context and question
        formatted_input = f"{self.image_context}\n\nQuestion: {question}\n\nAnswer:"
        
        # Reset history for fresh context
        self.reset_conversation()
        
        # Get response
        return self.get_response(formatted_input)
    
    def reset_conversation(self):
        """Reset the conversation history"""
        self.chat_history_ids = None
        return {"success": True, "message": "Conversation reset"}