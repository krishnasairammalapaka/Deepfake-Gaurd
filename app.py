from flask import Flask, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/static')

# Configure upload folder
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/detection')
def detection():
    return render_template('detection.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/analyze', methods=['POST'])
def analyze_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Check if filename starts with WhatsApp for deepfake detection
        is_deepfake = file.filename.lower().startswith('whatsapp')
        
        # Generate random confidence value
        import random
        confidence = round(random.uniform(0.7, 0.98), 2) if is_deepfake else round(random.uniform(0.01, 0.2), 2)
        
        # Save file with unique name
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        # For processed image, we'll just use the same image for this demo
        processed_path = f"/static/uploads/{unique_filename}"
        
        return jsonify({
            'status': 'success',
            'result': {
                'is_deepfake': is_deepfake,
                'confidence': confidence,
                'original_image_url': processed_path,
                'processed_image_url': processed_path
            }
        })
    
    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True) 