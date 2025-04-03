from unittest import TestCase

import mongomock
from flask import Flask
from flask_jwt_extended import JWTManager
from mongoengine import connect

from apps.data.model.user import User
from apps.services.auth.authservice import AuthService


class TestAuthService(TestCase):


    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config["TESTING"] = True
        cls.app.config["JWT_SECRET_KEY"] = "test_secret"
        cls.jwt = JWTManager(cls.app)
        connect('mongoenginetest', host='mongodb://localhost', mongo_client_class=mongomock.MongoClient)


    def setUp(self):
        self.app_context = self.app.app_context()
        self.app_context.push()
        User.objects.delete()

    def tearDown(self):
        self.app_context.pop()

    def test_that_registration_works_return_count_of_one(self):
        auth_service = AuthService()
        data = {"email": "test_email@gmail.com"}
        response, status = auth_service.register_account(data)
        response_json = response.get_json()

        assert status == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == 'test_email@gmail.com registered successfully'
        assert User.objects.count() == 1

    def test_that_an_already_registered_account_cannot_register_twice(self):
        auth_service = AuthService()
        data = {"email": "test_email@gmail.com"}
        response, status = auth_service.register_account(data)
        response_json = response.get_json()

        assert status == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == 'test_email@gmail.com registered successfully'

        data2 = {"email": "test_email@gmail.com"}
        response, status = auth_service.register_account(data2)
        response_json = response.get_json()

        assert status == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == "This account is already registered"


    def test_that_login_function_status_returns_200(self):
        auth_service = AuthService()
        data = {"email": "test_email@gmail.com"}
        response, status = auth_service.register_account(data)
        response_json = response.get_json()

        assert status == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == 'test_email@gmail.com registered successfully'

        data2 = {"email": "test_email@gmail.com"}
        response, status = auth_service.register_account(data2)
        response_json = response.get_json()

        assert status == 400
        assert response_json['status'] == 'error'
        assert response_json['message'] == "This account is already registered"


        auth_service = AuthService()
        data = {"email": "test_email@gmail.com"}
        response, status = auth_service.login(data)
        response_json = response.get_json()

        assert status == 200
        assert response_json['status'] == 'success'
        assert response_json['message'] == 'test_email@gmail.com login successful'



