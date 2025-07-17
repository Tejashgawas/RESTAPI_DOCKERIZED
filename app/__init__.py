from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask, jsonify
from app.utils.error_handlers import register_error_handlers
from flask_bcrypt import Bcrypt
from app.utils.oauth import configure_oauth
from dotenv import load_dotenv
import os
from app.config import DevelopmentConfig, TestConfig
from flasgger import Swagger


db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()


def create_app(testing=False):
    app = Flask(__name__)
    swagger = Swagger(app)
    
    
    if testing:
        app.config.from_object('app.config.TestConfig')
    else:
        app.config.from_object('app.config.DevelopmentConfig')

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    

    from app.models.user import User
    from app.models.book import Book
    

    
    # Import and register blueprints
    from app.routes.books import books_bp
    from app.routes.auth import auth_bp
    from app.routes.test_route import test_bp
    app.register_blueprint(books_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(test_bp)
    
    register_error_handlers(app)
    configure_oauth(app)

    @app.route('/')
    def home():
        return jsonify({
        "message": "Flask + SQLAlchemy API connected 🚀"
        })
    
    with app.app_context():
        db.create_all()
    
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.debug = True

    return app
