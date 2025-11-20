"""
Flask Application Factory
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from app.config import get_config
from app.extensions import init_extensions


def create_app(config_name=None):
    """
    Application factory pattern

    Args:
        config_name: Configuration to use (development, production, testing)

    Returns:
        Flask app instance
    """
    app = Flask(__name__)

    # Load configuration
    if config_name:
        app.config.from_object(f'app.config.{config_name.capitalize()}Config')
    else:
        app.config.from_object(get_config())

    # Initialize extensions
    init_extensions(app)

    # Register blueprints
    register_blueprints(app)

    # Setup logging
    setup_logging(app)

    # Register error handlers
    register_error_handlers(app)

    # Create upload directories
    create_upload_dirs(app)

    return app


def register_blueprints(app):
    """Register Flask blueprints"""
    from app.routes.auth import auth_bp
    from app.routes.students import students_bp
    from app.routes.jobs import jobs_bp
    from app.routes.mentors import mentors_bp
    from app.routes.messaging import messaging_bp
    from app.routes.courses import courses_bp
    from app.routes.social import social_bp
    from app.routes.ai_tools import ai_tools_bp

    # API version prefix
    api_prefix = f"/api/{app.config.get('API_VERSION', 'v1')}"

    app.register_blueprint(auth_bp, url_prefix=f'{api_prefix}/auth')
    app.register_blueprint(students_bp, url_prefix=f'{api_prefix}/students')
    app.register_blueprint(jobs_bp, url_prefix=f'{api_prefix}/jobs')
    app.register_blueprint(mentors_bp, url_prefix=f'{api_prefix}/mentors')
    app.register_blueprint(messaging_bp, url_prefix=f'{api_prefix}/messages')
    app.register_blueprint(courses_bp, url_prefix=f'{api_prefix}/courses')
    app.register_blueprint(social_bp, url_prefix=f'{api_prefix}/social')
    app.register_blueprint(ai_tools_bp, url_prefix=f'{api_prefix}/ai-tools')


def setup_logging(app):
    """Setup application logging"""
    if not app.debug and not app.testing:
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.mkdir('logs')

        # File handler
        file_handler = RotatingFileHandler(
            app.config.get('LOG_FILE', 'logs/collabio.log'),
            maxBytes=10240000,  # 10MB
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(getattr(logging, app.config.get('LOG_LEVEL', 'INFO')))
        app.logger.addHandler(file_handler)

        app.logger.setLevel(getattr(logging, app.config.get('LOG_LEVEL', 'INFO')))
        app.logger.info('Collabio startup')


def register_error_handlers(app):
    """Register error handlers"""
    from flask import jsonify

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        from app.extensions import db
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({'error': 'Access forbidden'}), 403

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request'}), 400


def create_upload_dirs(app):
    """Create upload directories if they don't exist"""
    upload_folder = app.config.get('UPLOAD_FOLDER', './uploads')
    categories = ['profiles', 'resumes', 'logos', 'courses', 'attachments']

    os.makedirs(upload_folder, exist_ok=True)
    for category in categories:
        os.makedirs(os.path.join(upload_folder, category), exist_ok=True)


# Initialize WebSocket events
from app.websockets import register_socket_events

def init_websocket(socketio):
    """Initialize WebSocket events"""
    register_socket_events(socketio)
