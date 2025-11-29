import os
from datetime import timedelta
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()


class Config:
    """Base configuration class with common settings."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DATABASE_HOST= os.getenv("DATABASE_HOST")
    DATABASE_USER = os.getenv("DATABASE_USER")
    DATABASE_PASSWORD =os.getenv("DATABASE_PASSWORD")
    DATABASE_NAME =os.getenv("DATABASE_NAME")
    DATABASE_PORT = os.getenv("DATABASE_PORT")
    encoded_password = quote_plus(DATABASE_PASSWORD)
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DATABASE_USER}:{encoded_password}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}" 
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
    }
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        seconds=int(os.getenv('JWT_REFRESH_TOKEN_EXPIRES', 2592000))
    )
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    
    # Application Configuration
    API_TITLE = os.getenv('API_TITLE', 'Task Manager API')
    API_VERSION = os.getenv('API_VERSION', '1.0.0')
    API_PREFIX = os.getenv('API_PREFIX', '/api')
    
    # CORS Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
    
    # Rate Limiting Configuration
    RATELIMIT_ENABLED = os.getenv('RATELIMIT_ENABLED', 'True').lower() == 'true'
    RATELIMIT_DEFAULT = os.getenv('RATELIMIT_DEFAULT', '100 per hour')
    RATELIMIT_STORAGE_URL = os.getenv('RATELIMIT_STORAGE_URL', 'memory://')
    
    # Pagination Configuration
    DEFAULT_PAGE_SIZE = int(os.getenv('DEFAULT_PAGE_SIZE', 20))
    MAX_PAGE_SIZE = int(os.getenv('MAX_PAGE_SIZE', 100))
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')
    
    ENV = os.getenv('FLASK_ENV', 'development')


class DevelopmentConfig(Config):
    """Development environment specific configuration."""
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Testing environment specific configuration."""
    TESTING = True
    DEBUG = True
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=300)
    RATELIMIT_ENABLED = False


class ProductionConfig(Config):
    """Production environment specific configuration."""
    DEBUG = False
    TESTING = False
    
    # Additional security headers for production
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config():
    """Get configuration based on FLASK_ENV environment variable."""
    env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])