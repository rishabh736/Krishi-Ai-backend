import os
import joblib
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)
CORS(app)

# 1. GEMINI AI SETUP
# Replace "YOUR_KEY_HERE" if you aren't using Render Environment Variables
API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyDtR5bheAVr4uCogM9em_fbx4Gb-nXb868")
genai.configure(api_key=API_KEY)
ai_model = genai.GenerativeModel('gemini-pro')

# 2. MODEL LOADING (With a fix for the [,,] error)
MODEL_PATH = 'model.pkl'

def create_model():
    # We provide REAL numbers here so there is no SyntaxError
    # Example: [Nitrogen, Phosphorus, Potassium, Temperature]
    X_train = np.array([,,])
    y_train = np.array(['Rice', 'Wheat', 'Maize'])
    m = RandomForestClassifier().fit(X_train, y_train)
    joblib.dump(m, MODEL_PATH)
    return m

# Attempt to load or create
try:
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
    else:
        model = create_model()
except:
    model = create_model()

# 3. ROUTES
@app.route('/')
def home():
    return jsonify({"status": "Krishi-Ai is Live", "message": "Ready for demo"})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        content = request.json
        # Expects: {"features":}
        raw_features = content.get('features')
        if not raw_features:
            return jsonify({"error": "No features provided"}), 400
            
        final_features = np.array(raw_features).reshape(1, -1)
        prediction = model.predict(final_features)
        return jsonify({"prediction": str(prediction)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get("message", "Hello")
        response = ai_model.generate_content(f"Agrotech context: {user_input}")
        return jsonify({"reply": response.text})
    except:
        return jsonify({"reply": "AI error - Check your API key"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
