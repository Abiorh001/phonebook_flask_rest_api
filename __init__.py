from flask import Flask, Blueprint, jsonify
from .models import db, User, Contact, shutdown_session
from flask_jwt_extended import JWTManager
import jwt
from datetime import timedelta


def create_app():
    app = Flask(__name__)

    

    app.config["JWT_SECRET_KEY"]= "jwt_secret_key"

    app.config["SECRET_KEY"]= "secret_key"
    app.config["SQLALCHEMY_DATABASE_URI"]= "mysql+pymysql://user:passwd@host_ip/db"

    app.config["JWT_ACCESS_TOKEN_EXPIRES"] =timedelta(minutes=60)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] =timedelta(minutes=60)


    db.init_app(app)
    with app.app_context():
        db.create_all()

    jwt = JWTManager(app)
    from jwt.exceptions import ExpiredSignatureError

    @app.errorhandler(ExpiredSignatureError)
    def handle_expired_signature_error(e):
        response = {'message': 'Token has expired'}
        return jsonify(response), 401
    
    # @jwt.expired_token_loader
    # def expired_token_callback():
    #     return jsonify({
    #     'status': 401,
    #     'message': 'The token has expired'
    # }), 401




    from .apis.user_api import user_api
    app.register_blueprint(user_api)

    from .apis.contact_api import contact_api
    app.register_blueprint(contact_api)

    app.teardown_request(shutdown_session)


    return app


