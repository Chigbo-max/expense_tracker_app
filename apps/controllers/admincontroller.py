from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from apps.services.admin.adminservice import AdminService
from helpers.decorators import admin_required

admin_view = Blueprint('admin_view', __name__)

admin_service = AdminService()


@admin_view.route('/admin/add-category', methods=['POST'])
@admin_required
@jwt_required()
def add_category():
    data = request.get_json()
    return admin_service.add_default_categories(data)

@admin_view.route('/admin/remove-category/<name>', methods=['PATCH'])
@admin_required
@jwt_required()
def remove_category(name):
    return admin_service.remove_default_categories(name.lower())


