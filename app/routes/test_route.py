from flask import Blueprint,jsonify

test_bp = Blueprint("test", __name__)

@test_bp.route("/api/ping")
def ping():
    return jsonify({"message": "pong"}), 200