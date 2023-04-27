from flask import Flask, Blueprint, jsonify
from .models import db, User, Contact, shutdown_session
from flask_jwt_extended import JWTManager
import jwt
from datetime import timedelta
from dotenv import load_dotenv
import os


def create_app():
    """Create a Flask app instance and initialize its configurations, database, JWT authentication,
    blueprints, and error handlers.
    
    Returns:
        Flask: A Flask app instance.
    """
    
    # Initializing the Flask app from Flask class
    app = Flask(__name__)

    # Load the environment variables from the .env file
    load_dotenv()

    # Set the JWT secret key
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY ")

    # Set the Flask secret key
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    # Set the SQLAlchemy database URI
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")

    # Set the access token and refresh token expiration time
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=60)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(minutes=60)

    # Initialize the database and create all tables
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Create an instance of JWTManager and pass our app as the parameter
    jwt = JWTManager(app)

    # Import and register the user_api blueprint
    from .apis.user_api import user_api
    app.register_blueprint(user_api)

    # Import and register the contact_api blueprint
    from .apis.contact_api import contact_api
    app.register_blueprint(contact_api)

    # Initialize the db.session.remove method to be called after each db.session.commit
    app.teardown_request(shutdown_session)

    # Return the Flask app instance
    return app
