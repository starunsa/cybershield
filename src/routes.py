"""
API Routes and Blueprints
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.auth import AuthService, require_auth
from src.models import User, ChatSession, ChatMessage, db
from src.chatbot import ChatbotService
from src.security_agent.main import SecurityAgent
from src.web_scanner import WebScanner
from datetime import datetime

# Create blueprints
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')
security_bp = Blueprint('security', __name__, url_prefix='/api/security')
user_bp = Blueprint('user', __name__, url_prefix='/api/user')

# Initialize services
chatbot_service = ChatbotService()
security_agent = SecurityAgent()
web_scanner = WebScanner()


# ==================== AUTH ROUTES ====================

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    full_name = data.get('full_name')
    
    result, status_code = AuthService.register_user(username, email, password, full_name)
    return jsonify(result), status_code


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    
    result, status_code = AuthService.login_user(username, password)
    return jsonify(result), status_code


@auth_bp.route('/validate', methods=['GET'])
@require_auth
def validate_token():
    """Validate current token and get user info"""
    user = AuthService.get_current_user()
    if user:
        return jsonify({
            'valid': True,
            'user': user.to_dict()
        }), 200
    return jsonify({'valid': False}), 401


# ==================== CHAT ROUTES ====================

@chat_bp.route('/greeting', methods=['POST'])
@require_auth
def get_greeting():
    """Get initial bot greeting"""
    user = AuthService.get_current_user()
    greeting = chatbot_service.get_greeting(user.username)
    return jsonify({
        'bot_name': chatbot_service.bot_name,
        'username': user.username,
        'greeting': greeting
    }), 200


@chat_bp.route('/send', methods=['POST'])
@require_auth
def send_message():
    """Send message to chatbot"""
    user = AuthService.get_current_user()
    data = request.get_json()
    
    if not data or 'message' not in data:
        return jsonify({'error': 'Message required'}), 400
    
    user_message = data.get('message')
    session_id = data.get('session_id')
    
    # Get or create session
    if session_id:
        session = ChatSession.query.get(session_id)
        if not session or session.user_id != user.id:
            return jsonify({'error': 'Invalid session'}), 403
    else:
        session = ChatSession(user_id=user.id, title='Chat Session')
        db.session.add(session)
        db.session.commit()
    
    # Process chat
    response = chatbot_service.process_chat(user_message, user.username)
    
    # Save messages to database
    user_msg = ChatMessage(session_id=session.id, sender='user', content=user_message)
    bot_msg = ChatMessage(session_id=session.id, sender='bot', content=response['bot_response'])
    
    db.session.add(user_msg)
    db.session.add(bot_msg)
    db.session.commit()
    
    return jsonify({
        'session_id': session.id,
        'bot_name': response['bot_name'],
        'username': response['username'],
        'user_message': response['user_message'],
        'bot_response': response['bot_response'],
        'timestamp': response['timestamp']
    }), 200


@chat_bp.route('/history/<int:session_id>', methods=['GET'])
@require_auth
def get_chat_history(session_id):
    """Get chat history for a session"""
    user = AuthService.get_current_user()
    session = ChatSession.query.get(session_id)
    
    if not session or session.user_id != user.id:
        return jsonify({'error': 'Invalid session'}), 403
    
    messages = ChatMessage.query.filter_by(session_id=session_id).order_by(ChatMessage.created_at).all()
    
    return jsonify({
        'session_id': session.id,
        'messages': [msg.to_dict() for msg in messages],
        'created_at': session.created_at.isoformat()
    }), 200


@chat_bp.route('/sessions', methods=['GET'])
@require_auth
def get_sessions():
    """Get all chat sessions for user"""
    user = AuthService.get_current_user()
    sessions = ChatSession.query.filter_by(user_id=user.id).order_by(ChatSession.created_at.desc()).all()
    
    return jsonify({
        'sessions': [session.to_dict() for session in sessions]
    }), 200


# ==================== SECURITY ROUTES ====================

@security_bp.route('/analyze-api', methods=['POST'])
@require_auth
def analyze_api():
    """Analyze API for security threats"""
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({'error': 'URL required'}), 400
    
    api_url = data.get('url')
    method = data.get('method', 'GET')
    headers = data.get('headers', {})
    payload = data.get('payload', {})
    
    try:
        report = security_agent.analyze_api(api_url, method=method, headers=headers, data=payload)
        return jsonify({
            'success': True,
            'report': report
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@security_bp.route('/scan-image', methods=['POST'])
@require_auth
def scan_image():
    """Scan container image for vulnerabilities"""
    data = request.get_json()
    
    if not data or 'image' not in data:
        return jsonify({'error': 'Image name required'}), 400
    
    image_name = data.get('image')
    
    try:
        report = security_agent.analyze_image(image_name)
        return jsonify({
            'success': True,
            'report': report
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@security_bp.route('/report', methods=['POST'])
@require_auth
def generate_report():
    """Generate comprehensive security report"""
    data = request.get_json()
    
    api_urls = data.get('api_urls', [])
    images = data.get('images', [])
    
    try:
        api_reports = [security_agent.analyze_api(url) for url in api_urls]
        image_reports = [security_agent.analyze_image(img) for img in images]
        
        report = security_agent.generate_report(api_reports, image_reports)
        
        return jsonify({
            'success': True,
            'report': report
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== USER ROUTES ====================

@user_bp.route('/profile', methods=['GET'])
@require_auth
def get_profile():
    """Get user profile"""
    user = AuthService.get_current_user()
    return jsonify({
        'user': user.to_dict()
    }), 200


@user_bp.route('/profile', methods=['PUT'])
@require_auth
def update_profile():
    """Update user profile"""
    user = AuthService.get_current_user()
    data = request.get_json()
    
    if 'full_name' in data:
        user.full_name = data['full_name']
    
    if 'email' in data:
        # Check if email already exists
        if User.query.filter_by(email=data['email']).filter(User.id != user.id).first():
            return jsonify({'error': 'Email already exists'}), 409
        user.email = data['email']
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Profile updated',
            'user': user.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@user_bp.route('/change-password', methods=['POST'])
@require_auth
def change_password():
    """Change user password"""
    user = AuthService.get_current_user()
    data = request.get_json()
    
    old_password = data.get('old_password')
    new_password = data.get('new_password')
    
    if not old_password or not new_password:
        return jsonify({'error': 'Old and new passwords required'}), 400
    
    if not user.check_password(old_password):
        return jsonify({'error': 'Invalid current password'}), 401
    
    try:
        user.set_password(new_password)
        db.session.commit()
        return jsonify({'message': 'Password changed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


def register_blueprints(app):
    """Register all blueprints with the app"""
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(security_bp)
    app.register_blueprint(user_bp)
