from unittest import TestCase

import mongomock
from flask import Flask
from flask_jwt_extended import JWTManager
from mongoengine import connect

from apps.data.model.user import User
from apps.services.user.userservice import UserService


class TestUserService(TestCase):
    pass

    # @classmethod
    # def setUpClass(cls):
    #     cls.app = Flask(__name__)
    #     cls.app.config["TESTING"] = True
    #     cls.app.config["JWT_SECRET_KEY"] = "test_secret"
    #     cls.jwt = JWTManager(cls.app)
    #     connect('mongoenginetest', host='mongomock://localhost', mongo_client_class=mongomock.MongoClient)
    #
    #
    # def setUp(self):
    #     self.app_context = self.app.app_context()
    #     self.app_context.push()
    #     User.objects.delete()
    #
    # def tearDown(self):
    #     self.app_context.pop()
    #
    #
    # def test_that_client_can_create_budge_return_count(self):
    #     user_service = UserService()
    #     data ={
    #         "user":"akerele@gmail.com",
    #         "categories":"clothings",
    #         "limit":"5000",
    #         "month":4,
    #         "year":2024}
    #
    #     response, status = user_service.create_budget(data)
    #     response_json = response.get_json()
    #
    #     assert status == 200
    #     assert response_json['status'] == "success"
    #     assert response_json['data'].count() == 1
