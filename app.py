
from flask import Flask
from flask_jwt_extended import JWTManager
from mongoengine import connect

from apps.controllers.admincontroller import admin_view
from apps.controllers.authcontroller import auth_view
from apps.controllers.usercontroller import user_view
from helpers.celerysetup import setup_celery
from helpers.config import Config

app = Flask(__name__)



connect(host=Config.MONGO_URI)

app.config.from_object(Config)

celery = setup_celery(app)

jwt = JWTManager(app)

app.register_blueprint(auth_view, url_prefix='/api')

app.register_blueprint(user_view, url_prefix='/api')

app.register_blueprint(admin_view,url_prefix='/api')




if __name__ == '__main__':
    app.run()



