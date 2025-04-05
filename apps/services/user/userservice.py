import traceback
from datetime import datetime

from flask import jsonify

from apps.data.model.budget import Budget
from apps.data.model.defaultcategories import DefaultCategories
from apps.data.model.expenses import Expenses
from apps.data.model.user import User
from apps.services.user.userserviceinterface import UserServiceInterface


class UserService(UserServiceInterface):
    def create_budget(self, user_identity, data):
        try:
            email = user_identity

            if not email:
                return jsonify({
                    'status': 'error',
                    'message': 'Not authorized to access this service'
                }), 400

            user = User.objects(email=email).first()


            default_categories =[category.name for category in DefaultCategories.objects()]

            valid_categories =  default_categories + user.custom_categories

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
                rollover_enabled = bool(data.get('rollover_enabled', False)),
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


    def update_budget(self, user_identity, data):
        email = user_identity

        try:
            user = User.objects(email=email).first()

            if user is None:
                return jsonify({
                    'status': 'error',
                    'message': 'User not found'
                }), 404

            budget = Budget.objects(user=user).first()
            if not budget:
                return jsonify({
                    "status": "error",
                    "message": "Not budget found"''
                }), 400

            updates={
                'set__last_updated': datetime.now(),
            }
            if 'limit' in data:
                updates['set__limit'] = float(data['limit'])
            if 'rollover_enabled' in data:
                updates['set__rollover_enabled'] = bool(data['rollover_enabled'])

            if updates:
                budget.update(**updates)
                budget.reload()

            return jsonify({
                'status': 'success',
                'data': {
                    'updated_limit': budget.limit,
                    'updated_rollover_enabled': budget.rollover_enabled,
                    'last_updated': budget.last_updated,
                    'message': 'budget updated successfully'
                }
            }), 200

        except Exception as e:
            return jsonify({
                'status': 'error',
                'message':f'Failed to update budget{str(e)}'
            }), 500


    def get_budget(self, user_identity):

        try:
            email = user_identity
            user = User.objects(email=email).first()
            if not user:
                return jsonify({
                    'status': 'error',
                    'message': 'User not found'
                }), 404

            current_month = datetime.now().month
            current_year = datetime.now().year

            budgets = Budget.objects(user=user, month=current_month, year=current_year).all()

            if not budgets:
                return jsonify({
                    'status': 'error',
                    'message': 'No budget found'
                }), 400

            budget_list = [
                {

                    'category' : budget.category,
                    'limit' : budget.limit,
                    'current_spending' : budget.current_spending or 0.0,
                    'month' : budget.month,
                    'year' : budget.year,

                 }
            for budget in budgets
            ]

            return jsonify({
                'status': 'success',
                'message': budget_list
            }), 200
        except Exception as e:
            print(traceback.format_exc())
            return jsonify({
                'status': 'error',
                'message':f'Failed to get budget{str(e)}'
            })

    def create_expenses(self, user_identity, data):
        email = user_identity

        if not email:
            return jsonify({
                'status': 'error',
                'message': 'Not authorized to access this service'
            }), 400
        try:
            user = User.objects(email=email).first()

            amount = data['amount']
            category = data['category']
            merchant = data['merchant']
            description = data['description']
            recipient = data['recipient']
            date = datetime.strptime(data['date'], '%Y-%m-%d')

            new_expense_entry = Expenses(
                user=user,
                amount = amount,
                category = category,
                merchant = merchant,
                description = description,
                recipient = recipient,
                date = date,
            )
            new_expense_entry.save()


            expense_month = datetime.now().month
            expense_year = datetime.now().year
            budget = Budget.objects(user=user, category=category, month=expense_month, year=expense_year).first()
            if budget:
                if budget.current_spending is None:
                    budget.update(set__current_spending = 0.0)
                    budget.reload()
                budget.update(inc__current_spending = amount)
                budget.reload()
                if budget.current_spending > budget.limit:
                    print(f"{budget.current_spending} is above limit for {expense_month},{expense_year} : {budget.limit}, category: {category}")

                    from app import celery

                    celery.tasks['apps.services.tasks.send_budget_exceeded_notification'].delay(
                        email=user_identity,
                        category=category,
                        limit=budget.limit,
                        current_spending=budget.current_spending
                    )


            return jsonify({
                'status': 'success',
                'data': {
                    'amount': amount,
                    'category': category,
                    'merchant': merchant,
                    'description': description,
                    'recipient': recipient,
                    'date': date,
                }
            }), 200
        except Exception as e:
            print(traceback.format_exc())
            return jsonify({
                'status': 'error',
                'message': f"Failed to create expenses; {str(e)}"
            }), 500




    def view_expenses(self, user_identity):
        try:
            email = user_identity
            if not email:
                return jsonify({
                    'status': 'error',
                    'message': 'Not authorized to access this service'
                }), 400

            user = User.objects(email=email).first()

            expenses = Expenses.objects()

            expenses_entry = [
                {
                    'amount': expense.amount,
                    'category': expense.category,
                    'merchant': expense.merchant,
                    'description': expense.description,
                    'recipient': expense.recipient,
                    'date': expense.date,
                }
                for expense in expenses
            ]

            return jsonify({
                "status": "success",
                "data": expenses_entry
            }), 200


        except Exception as e:
            return jsonify({
                    'status': 'error',
                    'message': f"Failed to get expenses; {str(e)}"
                }), 500


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