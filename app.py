"""
CyberShield - Production Grade Security Operations Platform
With Chatbot, Authentication, and Multi-User Support
"""
import os
import logging
from pathlib import Path
from flask import Flask, render_template, redirect, url_for, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from werkzeug.middleware.proxy_fix import ProxyFix
from dotenv import load_dotenv

from src.models import db
from src.config import get_config
from src.routes import register_blueprints

# Load environment variables
load_dotenv()


def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__, template_folder='templates', static_folder='static')

    config = get_config()
    app.config.from_object(config)
    app.config['JSON_SORT_KEYS'] = False
    app.config['PROPAGATE_EXCEPTIONS'] = True

    # Security proxy headers when running behind load balancers
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1)

    # Initialize extensions
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": config.CORS_ORIGINS}}, supports_credentials=True)
    jwt = JWTManager(app)

    @jwt.invalid_token_loader
    def invalid_token(reason):
        return jsonify({'error': reason, 'msg': reason}), 422

    @jwt.expired_token_loader
    def expired_token(jwt_header, jwt_payload):
        return jsonify({'error': 'Token has expired', 'msg': 'Token has expired'}), 401

    @jwt.unauthorized_loader
    def missing_token(reason):
        return jsonify({'error': reason, 'msg': reason}), 401

    # Register blueprints
    register_blueprints(app)

    # Create database tables if the SQLite database is missing
    with app.app_context():
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
        if db_uri.startswith('sqlite:'):
            db_path = db_uri.replace('sqlite:///', '')
            if not Path(db_path).exists():
                Path(db_path).parent.mkdir(parents=True, exist_ok=True)
                db.create_all()
        elif app.config['FLASK_ENV'] != 'production':
            db.create_all()

    @app.route('/')
    def index():
        """Login page"""
        return render_template('login.html')

    @app.route('/dashboard')
    def dashboard():
        """Dashboard page"""
        return render_template('dashboard.html')

    @app.route('/healthz')
    def healthz():
        """Health check endpoint for containers and Kubernetes"""
        return {'status': 'ok', 'service': 'cybershield'}, 200

    @app.errorhandler(404)
    def not_found(error):
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Endpoint not found'}), 404
        return redirect(url_for('index'))

    @app.errorhandler(Exception)
    def handle_exception(error):
        logging.exception('Unhandled exception: %s', error)
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Internal server error'}), 500
        return render_template('login.html'), 500

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('PORT', 5000)),
        debug=app.config.get('DEBUG', False)
    )
