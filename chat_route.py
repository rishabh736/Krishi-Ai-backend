from flask import Blueprint, request, jsonify
from services.ai_engine import ai_engine
from services.prediction_service import get_prediction

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_query = data.get("message")

        prediction = get_prediction(data)

    
        ai_response = ai_engine(prediction, user_query, mode="chat")

        return jsonify({
            "status": "success",
            "response": ai_response
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400
