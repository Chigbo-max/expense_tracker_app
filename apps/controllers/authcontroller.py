from flask import Blueprint, request
from apps.services.auth.authservice import AuthService

auth_view = Blueprint('auth_view', __name__)

authservice = AuthService()


@auth_view.route('/register-account', methods=['POST'])
def register_account():
    data = request.get_json()
    return authservice.register_account(data)


@auth_view.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return authservice.login(data)
