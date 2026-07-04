"""
Authentication Service
"""
import re
from functools import wraps
from flask import jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.models import User, db
from typing import Dict, Tuple, Optional

EMAIL_REGEX = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')

class AuthService:
    """Handle user authentication and authorization"""

    @staticmethod
    def validate_password(password: str) -> bool:
        if not password or len(password) < 8:
            return False
        if not re.search(r'[A-Za-z]', password):
            return False
        if not re.search(r'\d', password):
            return False
        return True

    @staticmethod
    def register_user(username: str, email: str, password: str, full_name: str = None) -> Tuple[Dict, int]:
        if not username or not email or not password:
            return {'error': 'Username, email, and password are required'}, 400

        if not EMAIL_REGEX.match(email):
            return {'error': 'A valid email address is required'}, 400

        if not AuthService.validate_password(password):
            return {'error': 'Password must be at least 8 characters and include letters and numbers'}, 400

        if User.query.filter_by(username=username).first():
            return {'error': 'Username already exists'}, 409

        if User.query.filter_by(email=email).first():
            return {'error': 'Email already exists'}, 409

        try:
            user = User(
                username=username,
                email=email,
                full_name=full_name or username
            )
            user.set_password(password)

            db.session.add(user)
            db.session.commit()

            return {
                'message': 'User registered successfully',
                'user': user.to_dict()
            }, 201
        except Exception as e:
            db.session.rollback()
            return {'error': 'Unable to register user'}, 500

    @staticmethod
    def login_user(username: str, password: str) -> Tuple[Dict, int]:
        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            return {'error': 'Invalid username or password'}, 401

        if not user.is_active:
            return {'error': 'User account is inactive'}, 401

        access_token = create_access_token(identity=str(user.id))

        return {
            'message': 'Login successful',
            'access_token': access_token,
            'user': user.to_dict()
        }, 200

    @staticmethod
    def get_current_user() -> Optional[User]:
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return None
            return db.session.get(User, int(user_id))
        except Exception:
            return None

    @staticmethod
    def validate_token() -> Tuple[bool, Optional[User]]:
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return False, None
            user = db.session.get(User, int(user_id))
            return True, user
        except Exception:
            return False, None


def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        user = AuthService.get_current_user()
        if not user:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function
