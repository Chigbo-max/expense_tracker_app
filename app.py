from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from mongoengine import connect
from helpers.config import Config


def create_app():
    app = Flask(__name__)

    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:19006", "exp://192.168.*", "exp://*.exp.host"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True,
        }
    })

    # connect(host=Config.MONGO_URI)

    connect(
        host=f"mongodb://{Config.MONGO_HOST}:{Config.MONGO_PORT}/ExpenseTracker")

    app.config.from_object(Config)

    jwt = JWTManager(app)

    from apps.controllers.authcontroller import auth_view
    from apps.controllers.usercontroller import user_view
    from apps.controllers.admincontroller import admin_view

    app.register_blueprint(auth_view, url_prefix='/api')
    app.register_blueprint(user_view, url_prefix='/api')
    app.register_blueprint(admin_view, url_prefix='/api')

    return app


app = create_app()
# flask run --host=0.0.0.0 --port=5000