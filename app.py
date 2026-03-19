import os
import joblib
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)
CORS(app)

# 1. AI SETUP
RAW_KEY = "AIzaSyDtR5bheAVr4uCogM9em_fbx4Gb-nXb868"
GEN_AI_KEY = os.environ.get("AIzaSyDtR5bheAVr4uCogM9em_fbx4Gb-nXb868", RAW_KEY)
genai.configure(api_key=GEN_AI_KEY)
ai_model = genai.GenerativeModel('gemini-pro')

# 2. MODEL SETUP
MODEL_PATH = 'model.pkl'
def create_dummy_model():
    # Placeholder data: 3 rows, 4 columns
    X = np.array([,,])
    y = np.array(['Rice', 'Wheat', 'Maize'])
    m = RandomForestClassifier().fit(X, y)
    joblib.dump(m, MODEL_PATH)
    return m

try:
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
    else:
        model = create_dummy_model()
except:
    model = create_dummy_model()

# 3. ROUTES
@app.route('/')
def health():
    return jsonify({"status": "Krishi-Ai Online"})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json['features']
        # Reshape for a single prediction
        features = np.array(data).reshape(1, -1)
        prediction = model.predict(features)
        return jsonify({"prediction": str(prediction)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/chat', methods=['POST'])
def chat():
    try:
        msg = request.json.get("message")
        response = ai_model.generate_content(f"Agrotech expert advice: {msg}")
        return jsonify({"reply": response.text})
    except:
        return jsonify({"reply": "AI error"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
