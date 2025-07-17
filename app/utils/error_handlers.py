from flask import jsonify
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            "status" :"error",
            "message" :"route not found",
            "data" : None
        }),404
    
    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({
            "status" :"error",
            "message" :"Method Not found",
            "data" : None
        }),405
    
    @app.errorhandler(500)
    def internal_server_error(e):
         return jsonify({
            "status" :"error",
            "message" :"Internal Server Error",
            "data" : None
        }),500
    
    @app.errorhandler(HTTPException)
    def handle_exception(e):
         return jsonify({
            "status" :"error",
            "message" : e.description,
            "data" : None
        }),e.code
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return jsonify({
                "status": e.code,
                "error": e.name,
                "message": e.description
            }), e.code
        # Non-HTTP error (e.g., db.commit() typo)
        return jsonify({
            "status": 500,
            "error": "Internal Server Error",
            "message": str(e)
        }), 500
