from flask import jsonify

from apps.data.model.defaultcategories import DefaultCategories
from apps.data.model.user import User
from apps.services.admin.adminserviceinterface import AdminServiceInterface


class AdminService(AdminServiceInterface):

    def close_account(self, data):
        pass

    def suspend_account(self, data):
        pass

    def activate_account(self, data):
        pass

    def view_all_users(self, data):
        pass

    def add_default_categories(self, data):

        try:
            category =  DefaultCategories(name=data['name'].lower().strip()).save()
            return jsonify({
                'status': 'success',
                'data': {
                    "added_category": category.name,
                    "message": "Added default categories",
                }

            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'Error adding default categories, {e}'
            }), 500

    def remove_default_categories(self, name):
        try:
            default_category = DefaultCategories.objects(name=name).first()

            if not default_category:
                return jsonify({
                    'status': 'error',
                    'message': f'Category {name} does not exist'
                }), 400

            default_category.delete()

            return jsonify({
                'status': 'success',
                'data': {
                    'deleted_category': default_category.name,
                    'message': "category successfully removed"
                }
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'Error removing default categories, {str(e)}'
            }), 500


