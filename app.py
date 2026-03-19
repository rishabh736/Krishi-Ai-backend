import os
import joblib
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)
CORS(app)

# --- 1. GEMINI AI SETUP ---
# It looks for "GEMINI_API_KEY" on Render. If not found, it uses your key as a backup.
RAW_KEY = "AIzaSyDtR5bheAVr4uCogM9em_fbx4Gb-nXb868"
GEN_AI_KEY = os.environ.get("AIzaSyDtR5bheAVr4uCogM9em_fbx4Gb-nXb868", RAW_KEY)

genai.configure(api_key=GEN_AI_KEY)
ai_model = genai.GenerativeModel('gemini-pro')

# --- 2. MODEL LOADING / AUTO-GENERATION ---
MODEL_PATH = 'model.pkl'
model = None

def create_dummy_model():
    # Fixed the empty array [,,] with sample data (N, P, K, Temp)
    X = np.array([,,])
    y = np.array(['Rice', 'Wheat', 'Maize'])
    m = RandomForestClassifier().fit(X, y)
    joblib.dump(m, MODEL_PATH)
    return m

if os.path.exists(MODEL_PATH):
    try:
        model = joblib.load(MODEL_PATH)
        print("✅ Real model.pkl loaded.")
    except Exception as e:
        print(f"⚠️ Could not load real model, generating dummy... {e}")
        model = create_dummy_model()
else:
    print("🚀 model.pkl not found. Generating temporary model for demo...")
    model = create_dummy_model()

# --- 3. ROUTES ---

@app.route('/')
def health():
    return jsonify({"status": "Krishi-Ai Online", "model": "Ready"})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        # Ensure 'features' exists in the incoming JSON
        if not data or 'features' not in data:
            return jsonify({"error": "Missing 'features' in request"}), 400
            
        features = np.array(data['features']).reshape(1, -1)
        prediction = model.predict(features) # Added to get the string result
        return jsonify({"prediction": str(prediction), "status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_msg = request.json.get("message")
        if not user_msg:
            return jsonify({"reply": "Please provide a message."})
            
        response = ai_model.generate_content(f"You are an Agrotech expert. User asks: {user_msg}")
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": "AI is currently unavailable."}), 500

if __name__ == "__main__":
    # Render uses the PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
