import os
from flask import Flask, jsonify
from flask_cors import CORS
from routes.predict_route import predict_bp
from routes.simulate_route import simulate_bp

app = Flask(__name__)
CORS(app) # Required for Vercel/Frontend communication

# Register Blueprints
app.register_blueprint(predict_bp)
app.register_blueprint(simulate_bp)

@app.route('/')
def health():
    return jsonify({
        "status": "Krishi-Ai Live",
        "ai_connected": os.environ.get("AIzaSyDtR5bheAVr4uCogM9em_fbx4Gb-nXb868") is not None
    })

if __name__ == "__main__":
    # Render uses the PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)