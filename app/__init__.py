"""
Guess The Word Game Application
A word-guessing game similar to Wordle, migrated from Java Spring Boot to Python Flask.
"""

from flask import Flask, url_for as flask_url_for, has_request_context
from config.settings import Config
import os


def create_app(config_class=Config):
    """Application factory pattern for creating Flask app instances."""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Handle proxy prefix for CloudFront/reverse proxy deployments
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    
    # Custom url_for that includes proxy prefix
    def proxy_url_for(endpoint, **values):
        """Custom url_for that adds proxy prefix for CloudFront deployment"""
        url = flask_url_for(endpoint, **values)
        proxy_prefix = app.config.get('PROXY_PREFIX', '/')
        
        # Always add proxy prefix when configured (CloudFront needs this)
        if proxy_prefix != '/' and not url.startswith(proxy_prefix):
            url = proxy_prefix.rstrip('/') + url
        
        return url
    
    # Make custom url_for available in templates
    @app.template_global()
    def url_for(endpoint, **values):
        return proxy_url_for(endpoint, **values)
    
    # Make custom url_for available in app context
    app.proxy_url_for = proxy_url_for
    
    # Register blueprints
    from app.controllers.game_controller import game_bp
    from app.controllers.home_controller import home_bp
    
    app.register_blueprint(home_bp)
    app.register_blueprint(game_bp, url_prefix='/game')
    
    return app
