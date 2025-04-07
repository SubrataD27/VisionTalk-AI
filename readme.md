# 🤖 VisionTalk AI - Advanced Visual Chatbot  
**_Made by Subrata Dhibar_**

---

## 🧠 Overview  
**VisionTalk AI** is a sophisticated visual chatbot platform that can analyze images and intelligently respond to questions about visual content. It combines cutting-edge computer vision and natural language processing to create an interactive assistant capable of understanding and discussing visual information.

---

## 🚀 Features
- 🖼️ **Image Analysis**: Upload images for instant object detection and scene classification  
- 📋 **Detailed Analysis Reports**: Get comprehensive breakdowns of image content with confidence scores  
- 🔍 **Visual Question Answering**: Ask questions about uploaded images and receive contextually relevant responses  
- 💬 **General Chatbot**: Engage in regular conversation with the AI assistant  

### 🤖 Multi-model AI Architecture:
- `ResNet50` – Image classification  
- `ViT-GPT2` – Image captioning  
- `BLIP` – Visual question answering  
- `DialoGPT` – Conversational chatbot

---

## 🛠️ Tech Stack
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript  
- **Backend**: Flask (Python)  
- **AI Models**: TensorFlow, PyTorch, Hugging Face Transformers  
- **Image Processing**: OpenCV, Pillow

---

## 🧰 Installation & Setup

### 🔁 Clone the repository
```bash
git clone https://github.com/SubrataD27/visiontalk-ai.git
cd visiontalk-ai
```

### 🧪 Create a virtual environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

### 📦 Install dependencies
```bash
pip install -r requirements.txt
```

### ▶️ Run the application
```bash
python app.py
```

Then open your browser and visit:
👉 http://localhost:5000

---

## 📁 Project Structure
```
visiontalk-ai/
├── app.py                    # Main Flask app
├── api_integrations.py       # External API integrations
├── models/                   # AI model files
│   ├── chat_model.py         # DialoGPT model
│   ├── image_model.py        # ResNet50 model
│   ├── image_captioning.py   # ViT-GPT2 captioning
│   └── visual_qa.py          # BLIP model
├── utils/
│   └── preprocessor.py       # Image preprocessing functions
├── static/
│   ├── css/
│   │   └── style.css         # Custom styling
│   ├── js/
│   │   └── script.js         # Client-side JS logic
│   └── images/               # UI graphics & static icons
├── templates/
│   └── index.html            # Main frontend template
├── uploads/                  # Temporary uploaded image storage
└── requirements.txt          # Python dependencies
```

---

## 🧑‍💻 Usage
- **Upload an Image**: Click the "Upload" button to select an image
- **View Analysis**: The system processes the image and displays analysis results
- **Ask Questions**: Type questions about the image in the chatbot
- **Chat Freely**: Talk casually with the AI beyond image-related queries

---

## 📸 Screenshots
(Add actual screenshots here)
- 📍 Main Dashboard
- 🧠 Image Analysis Results
- ❓ Visual Question Answering Interface

---

## 🔮 Future Enhancements
- 🎥 Support for video analysis
- 🌍 Multi-language support
- 😊 Advanced emotion recognition
- 🔐 User authentication system
- 💾 Saved conversation history
- 📱 Mobile app version

---

## 🙏 Acknowledgments
- Hugging Face for pre-trained transformer models
- TensorFlow & PyTorch for AI frameworks
- Flask for the web backend

---

## 📄 License
This project is licensed under the MIT License. See the LICENSE file for details.

---

## 🤝 Contributing
Contributions are welcome!
Feel free to fork the repository and submit a Pull Request.

---

## 👨‍💻 Author
- Subrata Dhibar
- [GitHub Profile](https://github.com/SubrataD27)