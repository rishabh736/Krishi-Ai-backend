import sys
import os
from flask import Flask, jsonify
from flask_cors import CORS

# --- 1. THE MODULE PATH FIX ---
# This ensures Python can see the 'routes' and 'services' folders 
# even when running on different servers like Render.
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# --- 2. IMPORT YOUR BLUEPRINTS ---
# Note: Ensure these variable names (predict_bp, etc.) match 
# what you wrote inside the route files.
try:
    from routes.predict_route import predict_bp
    from routes.simulate_route import simulate_bp
    from routes.chat_route import chat_bp
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("👉 Make sure you have empty __init__.py files in 'routes' and 'services' folders.")

# --- 3. INITIALIZE APP ---
app = Flask(__name__)

# Allow Cross-Origin Resource Sharing (so your Vercel/Frontend can talk to this API)
CORS(app)

# --- 4. REGISTER BLUEPRINTS ---
# This connects your modular files to the main app
app.register_blueprint(predict_bp)
app.register_blueprint(simulate_bp)
app.register_blueprint(chat_bp)

# --- 5. HEALTH CHECK ROUTE ---
@app.route('/')
def health_check():
    return jsonify({
        "status": "Krishi-Ai Backend is Online",
        "api_version": "1.0.0",
        "ai_status": "Connected" if os.environ.get("AIzaSyDtR5bheAVr4uCogM9em_fbx4Gb-nXb868") else "Key Missing"
    })

# --- 6. ERROR HANDLING ---
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Route not found. Check your URL (e.g., /predict or /simulate)"}), 404

# --- 7. START COMMAND FOR LOCAL & RENDER ---
if __name__ == "__main__":
    # Render uses the 'PORT' environment variable, defaulting to 5000 locally
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 Krishi-Ai starting on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=True)
