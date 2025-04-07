🤖 VisionTalk AI - Advanced Visual Chatbot

Overview
VisionTalk AI is a sophisticated visual chatbot platform that can analyze images and intelligently respond to questions about visual content. This project combines state-of-the-art computer vision with natural language processing to create an interactive AI assistant capable of understanding and discussing visual information.
Features

🖼️ Image Analysis: Upload images for instant object detection and scene classification
📋 Detailed Analysis Reports: Get comprehensive breakdowns of image content with confidence scores
🔍 Visual Question Answering: Ask questions about uploaded images and receive contextually relevant responses
💬 General Chatbot: Engage in regular conversation with the AI assistant
📊 Multi-model Architecture: Utilizes several AI models for enhanced accuracy:

ResNet50 for image classification
ViT-GPT2 for image captioning
BLIP for visual question answering
DialoGPT for conversational responses



Tech Stack

Frontend: HTML5, CSS3, Bootstrap 5, JavaScript
Backend: Flask (Python)
AI Models: TensorFlow, PyTorch, Hugging Face Transformers
Image Processing: OpenCV, Pillow

Installation

Clone the repository:
bashCopygit clone https://github.com/SubrataD27/visiontalk-ai.git
cd visiontalk-ai

Create a virtual environment:
bashCopypython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:
bashCopypip install -r requirements.txt

Run the application:
bashCopypython app.py

Open your browser and navigate to http://localhost:5000

Project Structure
Copyvisiontalk-ai/
├── app.py                  # Main Flask application
├── models/
│   ├── chat_model.py       # Conversational AI model
│   ├── image_model.py      # Image classification model
│   ├── image_captioning.py # Image captioning model
│   └── visual_qa.py        # Visual question answering model
├── utils/
│   └── preprocessor.py     # Image preprocessing utilities
├── static/
│   ├── css/
│   │   └── style.css       # Custom styling
│   ├── js/
│   │   └── script.js       # Frontend logic
│   └── images/             # Static images and icons
├── templates/
│   └── index.html          # Main application template
├── uploads/                # Temporary storage for uploaded images
└── api_integrations.py     # External API integrations
Usage

Upload an Image: Click the upload button and select an image from your computer
View Analysis: The system will process the image and display object detection results
Ask Questions: Type questions about the image in the chat box
Chat with AI: Engage in regular conversation with the AI assistant

Screenshots
Show Image
Main Dashboard
Show Image
Image Analysis Results
Show Image
Visual Question Answering
Future Enhancements

 Support for video analysis
 Multi-language support
 Advanced emotion recognition
 User authentication system
 Saved conversation history
 Mobile application

Acknowledgments

Hugging Face for providing pre-trained models
TensorFlow and PyTorch for ML frameworks
Flask for the web framework

License
This project is licensed under the MIT License - see the LICENSE file for details.
Author
Subrata Dhibar

Contributing
Contributions are welcome! Please feel free to submit a Pull Request.