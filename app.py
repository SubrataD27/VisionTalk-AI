import os
import uuid
import re
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from models.chat_model import ChatModel
from models.image_model import ImageAnalyzer
from models.image_captioning import ImageCaptioner
from utils.preprocessor import preprocess_image
from utils.api_integrations import get_weather

# Try to import the VisualQA model, use standard chat model as fallback
try:
    from models.visual_qa import VisualQA
    visual_qa = VisualQA()
    use_visual_qa = visual_qa.is_available()
except Exception:
    print("Visual QA model not available, using fallback method")
    use_visual_qa = False

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize models
chat_model = ChatModel()
image_analyzer = ImageAnalyzer()
image_captioner = ImageCaptioner()

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat requests"""
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({"success": False, "error": "No message provided"})
    
    # Check if it's a weather query
    weather_pattern = re.compile(r'weather\s+in\s+([a-zA-Z\s]+)', re.IGNORECASE)
    weather_match = weather_pattern.search(user_message)
    
    if weather_match:
        city = weather_match.group(1).strip()
        weather_data = get_weather(city)
        
        if weather_data["success"]:
            weather_response = f"Weather in {weather_data['city']}, {weather_data['country']}: " \
                               f"{weather_data['description']}. " \
                               f"Temperature: {weather_data['temperature']}°C " \
                               f"(feels like {weather_data['feels_like']}°C). " \
                               f"Humidity: {weather_data['humidity']}%. " \
                               f"Wind speed: {weather_data['wind_speed']} m/s."
            return jsonify({"success": True, "response": weather_response})
        else:
            return jsonify({"success": True, "response": f"I couldn't find weather information for {city}. {weather_data.get('error', '')}"})
    
    # Get response from chat model for non-weather queries
    result = chat_model.get_response(user_message)
    return jsonify(result)

@app.route('/reset', methods=['POST'])
def reset():
    """Reset the conversation"""
    return jsonify(chat_model.reset_conversation())

@app.route('/analyze-image', methods=['POST'])
def analyze_image():
    """Analyze an uploaded image"""
    if 'image' not in request.files:
        return jsonify({"success": False, "error": "No image provided"})
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"success": False, "error": "No image selected"})
    
    try:
        # Generate a unique filename
        filename = str(uuid.uuid4()) + os.path.splitext(secure_filename(file.filename))[1]
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Preprocess the image
        preprocess_image(file_path)
        
        # Analyze the image
        result = image_analyzer.analyze_image(file_path)
        
        # Get caption for additional context
        caption_result = image_captioner.generate_caption(file_path)
        if caption_result["success"]:
            result["caption"] = caption_result["caption"]
        
        # Add image path to result for frontend display
        if result["success"]:
            result["image_path"] = os.path.join('uploads', filename)
            
            # Generate image context and store it in chat model
            context = create_image_context(result)
            chat_model.set_image_context(context)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

def create_image_context(analysis_result):
    """Create context information from image analysis"""
    context = "I am looking at an image. "
    context += analysis_result["summary"] + " "
    
    if "caption" in analysis_result:
        context += f"The caption for this image is: {analysis_result['caption']}. "
    
    context += "Other objects detected in the image: "
    for desc in analysis_result["descriptions"][1:]:
        context += f"{desc['label']} ({desc['confidence']:.1f}%), "
    
    context += "\nI'll answer questions about this image based on what I can see."
    return context

@app.route('/get-caption', methods=['POST'])
def get_caption():
    """Generate a caption for an image"""
    if 'image' not in request.files:
        return jsonify({"success": False, "error": "No image provided"})
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"success": False, "error": "No image selected"})
    
    try:
        # Generate a unique filename
        filename = str(uuid.uuid4()) + os.path.splitext(secure_filename(file.filename))[1]
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Generate caption
        result = image_captioner.generate_caption(file_path)
        
        # Add image path to result for frontend display
        if result["success"]:
            result["image_path"] = os.path.join('uploads', filename)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/image-question', methods=['POST'])
def image_question():
    """Answer questions about an image"""
    data = request.json
    image_path = data.get('image_path', '')
    question = data.get('question', '')
    
    if not image_path or not question:
        return jsonify({"success": False, "error": "Image path and question required"})
    
    try:
        # Get the full path to the image
        full_path = os.path.join('static', image_path)
        
        # Use specialized visual QA model if available
        if use_visual_qa:
            result = visual_qa.answer_question(full_path, question)
            if result["success"]:
                return jsonify({
                    "success": True,
                    "response": result["answer"]
                })
        
        # Fallback to chat model with image context
        result = chat_model.get_response_with_image_context(question)
        return jsonify(result)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)