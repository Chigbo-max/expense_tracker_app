
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from apps.services.user.userservice import UserService

user_view = Blueprint('user_view', __name__)

user_service = UserService()

@user_view.route('/create-budget', methods=['POST'])
@jwt_required()
def create_budget():
    data = request.get_json()
    user_identity = get_jwt_identity()
    return user_service.create_budget(user_identity, data)


@user_view.route('/add-a-category', methods=['POST'])
@jwt_required()
def add_category():
    user_identity = get_jwt_identity()
    data = request.get_json()
    return user_service.add_category(user_identity, data)

@user_view.route('/get-all-categories', methods=['GET'])
@jwt_required()
def view_categories():
    user_identity = get_jwt_identity()
    return user_service.view_categories(user_identity)


@user_view.route('/create-expenses', methods=['POST'])
@jwt_required()
def create_expenses():
    user_identity = get_jwt_identity()
    data = request.get_json()
    return user_service.create_expenses(user_identity, data)


@user_view.route('/view-expenses', methods=['GET'])
@jwt_required()
def view_expenses():
    user_identity = get_jwt_identity()
    return user_service.view_expenses(user_identity)




