from flask import Flask
from flask_jwt_extended import JWTManager
from mongoengine import connect

from helpers.config import Config

app = Flask(__name__)

connect(host=Config.MONGO_URI)

app.config.from_object(Config)

jwt = JWTManager(app)

# app.register_blueprint


if __name__ == '__main__':
    app.run()



