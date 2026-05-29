"""
Authentication Service
"""
from functools import wraps
from flask import request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.models import User, db
from typing import Dict, Tuple

class AuthService:
    """Handle user authentication and authorization"""
    
    @staticmethod
    def register_user(username: str, email: str, password: str, full_name: str = None) -> Tuple[Dict, int]:
        """Register a new user"""
        # Validate input
        if not username or not email or not password:
            return {'error': 'Username, email, and password are required'}, 400
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return {'error': 'Username already exists'}, 409
        
        if User.query.filter_by(email=email).first():
            return {'error': 'Email already exists'}, 409
        
        # Create new user
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
            return {'error': str(e)}, 500
    
    @staticmethod
    def login_user(username: str, password: str) -> Tuple[Dict, int]:
        """Authenticate user and return JWT token"""
        user = User.query.filter_by(username=username).first()
        
        if not user or not user.check_password(password):
            return {'error': 'Invalid username or password'}, 401
        
        if not user.is_active:
            return {'error': 'User account is inactive'}, 401
        
        # Generate JWT token
        access_token = create_access_token(identity=user.id)
        
        return {
            'message': 'Login successful',
            'access_token': access_token,
            'user': user.to_dict()
        }, 200
    
    @staticmethod
    def get_current_user() -> User:
        """Get current authenticated user"""
        try:
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            return user
        except Exception as e:
            return None
    
    @staticmethod
    def validate_token(token: str) -> Tuple[bool, User]:
        """Validate JWT token and return user"""
        try:
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            return True, user
        except Exception as e:
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
