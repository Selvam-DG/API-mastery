import logging
import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import database_exists, create_database
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.config import get_config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()
cors = CORS()
limiter = Limiter( key_func=get_remote_address, default_limits=["100 per hour"])

def create_app(config_name=None):
    """
    Application   
    """
    app = Flask(__name__)
    
    # Load Configuration
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app.config.from_object(get_config())
    
    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app)
    jwt.init_app(app=app)
    bcrypt.init_app(app)
    cors.init_app(app, origins=app.config['CORS_ORIGINS'])
    
    db_url = app.config['SQLALCHEMY_DATABASE_URI']
    if not database_exists(db_url):
        create_database(db_url)
        app.logger.info(f"Database created")
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Initialize rate limiter if enable
    if app.config.get('RATELIMIT_ENABLED', True):
        limiter.init_app(app)
    
    # Configure logging
    configure_logging(app)
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register JWT callbacks
    register_jwt_callbacks(app)
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint."""
        return jsonify({
            'status': 'healthy',
            'api_version': app.config['API_VERSION']
        }), 200
    
    # API info endpoint
    @app.route(f"{app.config['API_PREFIX']}", methods=['GET'])
    def api_info():
        """API information endpoint."""
        return jsonify({
            'title': app.config['API_TITLE'],
            'version': app.config['API_VERSION'],
            'endpoints': {
                'auth': f"{app.config['API_PREFIX']}/auth",
                'projects': f"{app.config['API_PREFIX']}/projects",
                'tasks': f"{app.config['API_PREFIX']}/tasks"
            }
        }), 200
    
    return app


def configure_logging(app):
    """
    Configure application logging.
    """
    log_level = getattr(logging, app.config['LOG_LEVEL'].upper(), logging.INFO)
    
    # Create logs directly if it doesn't exist
    log_file = app.config.get('LOG_FILE')
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
    # Configure logging format
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file) if log_file else logging.StreamHandler(),
            logging.StreamHandler()
        ]
    )
    app.logger.setLevel(log_level)
    app.logger.info(f'Application started in {app.config["ENV"]} mode')
    
def register_blueprints(app):
    """
    Register app blueprints.
    """
    from app.routes.auth import auth_bp
    from app.routes.projects import projects_bp
    from app.routes.tasks import tasks_bp
    
    # Register blueprints with API prefix
    api_prefix = app.config['API_PREFIX']
    app.register_blueprint(auth_bp, url_prefix=f'{api_prefix}/auth')
    app.register_blueprint(projects_bp, url_prefix=f'{api_prefix}/projects')
    app.register_blueprint(tasks_bp, url_prefix=f'{api_prefix}/tasks')


def register_error_handlers(app):
    """
    Register global error handlers.
    """
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error': 'Bad Request',
            'message': str(error)
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'error': 'Unauthorized',
            'message': 'Authentication required'
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'error': 'Forbidden',
            'message': 'You do not have permission to access this resource'
        }), 403
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found'
        }), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'error': 'Method Not Allowed',
            'message': 'The method is not allowed for the requested URL'
        }), 405
    
    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            'error': 'Unprocessable Entity',
            'message': 'The request was well-formed but contains semantic errors'
        }), 422
    
    @app.errorhandler(429)
    def ratelimit_handler(error):
        return jsonify({
            'error': 'Too Many Requests',
            'message': 'Rate limit exceeded. Please try again later.'
        }), 429
    
    @app.errorhandler(500)
    def internal_server_error(error):
        app.logger.error(f'Internal Server Error: {str(error)}')
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred'
        }), 500


def register_jwt_callbacks(app):
    """Register JWT callbacks for custom responses."""
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'error': 'Token Expired',
            'message': 'The token has expired'
        }), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({
            'error': 'Invalid Token',
            'message': 'Token validation failed'
        }), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            'error': 'Authorization Required',
            'message': 'Request does not contain a valid token'
        }), 401
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'error': 'Token Revoked',
            'message': 'The token has been revoked'
        }), 401
    
    