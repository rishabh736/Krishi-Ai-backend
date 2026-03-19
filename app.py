import os
import sys
import joblib
from flask import Flask, request, jsonify
from flask_cors import CORS

# 1. SETUP
app = Flask(__name__)
CORS(app)

# 2. LOAD MODEL (Make sure model.pkl is in the same folder as app.py)
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')
model = None
if os.path.exists(MODEL_PATH):
    try:
        model = joblib.load(MODEL_PATH)
        print("✅ Model loaded successfully")
    except Exception as e:
        print(f"❌ Model load error: {e}")

# 3. ROUTES (No imports needed!)

@app.route('/')
def home():
    return jsonify({"status": "Krishi-Ai is LIVE", "model_loaded": model is not None})

@app.route('/predict', methods=['POST'])
def predict():
    if not model:
        return jsonify({"error": "Model not loaded on server"}), 500
    
    data = request.json
    # Logic: Get data from frontend (example:)
    # features = [data['temp'], data['rain'], data['hum'], data['wind']]
    # prediction = model.predict([features])
    return jsonify({"prediction": "Rice", "confidence": "92%"})

@app.route('/chat', methods=['POST'])
def chat():
    # Your Gemini AI logic here
    return jsonify({"response": "I am your Agriculture AI assistant."})

# 4. RENDER START LOGIC
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
