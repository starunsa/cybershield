"""
Application Configuration
"""
import os
from datetime import timedelta


def _parse_bool(value: str, default: bool = False) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in ('1', 'true', 'yes', 'on')


def _parse_list(value: str, default=None):
    if default is None:
        default = ['*']
    if not value:
        return default
    return [item.strip() for item in value.split(',') if item.strip()]


class Config:
    """Base configuration"""
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = _parse_bool(os.getenv('DEBUG', 'False'))

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///instance/cybershield.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-super-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)

    SESSION_COOKIE_SECURE = _parse_bool(os.getenv('SESSION_COOKIE_SECURE', 'True'))
    SESSION_COOKIE_HTTPONLY = _parse_bool(os.getenv('SESSION_COOKIE_HTTPONLY', 'True'))
    SESSION_COOKIE_SAMESITE = os.getenv('SESSION_COOKIE_SAMESITE', 'Lax')

    CORS_ORIGINS = _parse_list(os.getenv('CORS_ORIGINS', '*'))

    APP_NAME = 'CyberShield'
    APP_VERSION = '1.0.0'
    PREFERRED_URL_SCHEME = 'https'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_ECHO = False
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    JWT_SECRET_KEY = 'test-secret-key'
    DEBUG = True


def get_config():
    env = os.getenv('FLASK_ENV', 'development')
    config_map = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
    }
    return config_map.get(env, DevelopmentConfig)
