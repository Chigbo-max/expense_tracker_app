import traceback
from datetime import timedelta

from flask import jsonify
from flask_jwt_extended import create_access_token, create_refresh_token

from apps.data.model.status import AccountStatus
from apps.data.model.user import User
from apps.services.auth.authInterface import AuthInterface


class AuthService(AuthInterface):

    def register_account(self, data):
        try:
            if User.objects(email=data['email']).first():
                return jsonify({f"status": "error", "message": "This account is already registered"}), 400

            email = data['email'].strip().lower()

            existing_admin = User.objects(role="admin").first()
            role = "admin" if not existing_admin else "user"

            user = User(email=email, role=role, status = AccountStatus.ACTIVE)
            user.save()

            access_token = create_access_token(identity=email, expires_delta=timedelta(minutes=40))
            refresh_token = create_refresh_token(identity=email, expires_delta=timedelta(days=2))
            return jsonify({f"status": "success",
                            "message": f"{email} registered successfully",
                            "role": role,
                            "access_token": access_token,
                            "refresh_token": refresh_token}), 200

        except Exception as e:
            return jsonify({f"status": "error", "message": str(e)}), 500

    def login(self, data):

        try:

            email = data['email'].strip().lower()

            user = User.objects(email=email).first()

            if not user:
                return jsonify({f"status": "error", "message": "This account is not registered"}), 400

            if user.status != AccountStatus.ACTIVE:
                return jsonify({f"status": "error", "message": "This account is not active please contact support"}), 400


            access_token = create_access_token(identity=email, expires_delta=timedelta(minutes=40))
            refresh_token = create_refresh_token(identity=email, expires_delta=timedelta(days=2))

            return jsonify({f"status": "success",
                            "message": f"{email} login successful",
                            "access_token": access_token,
                            "refresh_token": refresh_token
                            }), 200

        except Exception as e:
            print(traceback.format_exc())
            return jsonify({f"status": "error", "message": str(e)}), 500