import sys
import os
from flask import Flask, jsonify
from flask_cors import CORS

# 1. FORCE PYTHON TO SEE YOUR FOLDERS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

app = Flask(__name__)
CORS(app)

# 2. DEFINE BLUEPRINTS AS NONE FIRST (Prevents NameError)
predict_bp = None
simulate_bp = None
chat_bp = None

# 3. ATTEMPT IMPORTS
try:
    from routes.predict_route import predict_bp
    from routes.simulate_route import simulate_bp
    from routes.chat_route import chat_bp
    
    # 4. ONLY REGISTER IF IMPORTS WORKED
    if predict_bp:
        app.register_blueprint(predict_bp)
    if simulate_bp:
        app.register_blueprint(simulate_bp)
    if chat_bp:
        app.register_blueprint(chat_bp)
        
except ImportError as e:
    print(f"❌ IMPORT FAILED: {e}")
    print("👉 Check: Do you have __init__.py in your folders?")

@app.route('/')
def home():
    return jsonify({"status": "Krishi-Ai is running!"})

if __name__ == "__main__":
    # This is for local testing: python app.py
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
