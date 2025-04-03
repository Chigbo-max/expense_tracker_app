import traceback
from datetime import datetime

from flask import jsonify

from apps.data.model.budget import Budget
from apps.data.model.defaultcategories import DefaultCategories
from apps.data.model.user import User
from apps.services.user.userserviceinterface import UserServiceInterface


class UserService(UserServiceInterface):
    def create_budget(self, user_identity, data):
        try:
            email = user_identity
            print("found email:" , email)

            if not email:
                return jsonify({
                    'status': 'error',
                    'message': 'Not authorized to access this service'
                }), 400

            user = User.objects(email=email).first()

            print("user found: ", user.email)

            default_categories =[category.name for category in DefaultCategories.objects()]
            print("default categories: ", default_categories)

            valid_categories =  default_categories + user.custom_categories
            print("valid_categories: ", valid_categories)

            if data['category'] not in valid_categories:
                return jsonify({
                    'status': 'error',
                    'message': 'Invalid category provided'
                }), 400

            budget = Budget(
                user=user,
                category = data['category'],
                limit = data['limit'],
                month = data.get('month', datetime.now().month),
                year = data.get('year', datetime.now().year),
            ).save()

            return jsonify({
                'status': 'success',
                'data': {
                    "category": budget.category,
                    "limit": budget.limit,
                    "month": budget.month,
                    "year": budget.year,
                    "message": "budget created successfully"
                }
            }), 200

        except Exception as e:
            print(traceback.format_exc())
            return jsonify({
                'status': 'error',
                'message': str(e)
            }), 500





    def create_expenses(self, user_identity, data):
        pass

    def view_expenses(self, user_identity):
        pass

    def add_category(self, user_identity, data):
        email = user_identity
        try:
            user = User.objects(email=email).first()
            if user is None:
                return jsonify({
                    'status': 'error',
                    'message': 'Not authorized to access this service'
                }), 400
            new_category = data['name'].lower().strip()
            default_categories = [category.name.lower() for category in DefaultCategories.objects()]
            if new_category in user.custom_categories or new_category in default_categories:
                return jsonify({
                    'status': 'error',
                    'message': 'Category already exists'
                }), 400
            user.update(push__custom_categories=new_category)
            return jsonify({
                    'status': 'success',
                    'data': {
                        "new_category": new_category,
                        "message": "New category added successfully"
                    }
                }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f"Failed to add category; {str(e)}"
            }), 500


    def view_categories(self, user_identity):

        try:
            email = user_identity

            user = User.objects(email=email).first()
            if user is None:
                return jsonify({
                    'status': 'error',
                    'message': 'Not authorized to access this service'
                }), 400

            all_categories = [category.name for category in DefaultCategories.objects] + user.custom_categories

            return jsonify({
                'status': 'success',
                'data': {
                    "all_categories": all_categories,
                }
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f"Failed to get categories; {str(e)}"
            })