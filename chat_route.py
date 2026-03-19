from flask import Blueprint, request, jsonify
from services.ai_engine import ai_engine
from services.prediction_service import get_prediction

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_query = data.get("message")

        # 1. Get current context (Optional: helps the AI know what's in the field)
        # We pass dummy/current data to get_prediction to give AI context
        prediction = get_prediction(data)

        # 2. Call the AI Engine in 'chat' mode
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