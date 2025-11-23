#!/usr/bin/env python3
"""
Guess The Word Game Application Entry Point

This is the main entry point for the Guess The Word word-guessing game application.
It creates and configures the Flask application instance and starts the
development server when run directly.

The application is a word-guessing game similar to Wordle, where players
attempt to guess a hidden word within a limited number of attempts. It was
successfully migrated from Java Spring Boot to Python Flask while maintaining
100% functional equivalence.

Usage:
    Development server:
        $ python app.py
        
    Production server:
        $ gunicorn -w 4 -b 0.0.0.0:8000 app:app
        
    With proxy configuration:
        $ APPLICATION_ROOT=/proxy/5000 PREFERRED_URL_SCHEME=https python app.py

Environment Variables:
    FLASK_ENV: Application environment (development/testing/production)
    SECRET_KEY: Secret key for session encryption (required in production)
    PORT: Port number for the server (default: 5000)
    APPLICATION_ROOT: Root path for proxy deployments (e.g., /proxy/5000)
    PREFERRED_URL_SCHEME: URL scheme for proxy deployments (http/https)

Example:
    >>> from app import app
    >>> app.config['TESTING']
    False
    >>> with app.test_client() as client:
    ...     response = client.get('/')
    ...     response.status_code
    200
"""

import os
from app import create_app
from config.settings import config


def get_config_name() -> str:
    """
    Determine the configuration name based on environment variables.
    
    Returns:
        str: Configuration name ('development', 'testing', 'production')
             Defaults to 'development' if FLASK_ENV is not set
    """
    return os.environ.get('FLASK_ENV', 'development')


def get_port() -> int:
    """
    Get the port number from environment variables.
    
    Returns:
        int: Port number for the server, defaults to 5000
    """
    return int(os.environ.get('PORT', 5000))


def print_startup_info(config_name: str, port: int, debug: bool) -> None:
    """
    Print startup information to the console.
    
    Args:
        config_name (str): Name of the configuration being used
        port (int): Port number the server will listen on
        debug (bool): Whether debug mode is enabled
    """
    print("🎮 Starting Guess The Word Game Server...")
    print(f"📍 Environment: {config_name}")
    print(f"🌐 Port: {port}")
    print(f"🔧 Debug: {debug}")
    
    # Show proxy configuration if set
    app_root = os.environ.get('APPLICATION_ROOT')
    url_scheme = os.environ.get('PREFERRED_URL_SCHEME')
    if app_root or url_scheme:
        print(f"🔗 Proxy Config: URLs will include {app_root or '/'} when accessed locally")
        print(f"🌐 CloudFront URLs: Proxy will handle prefix automatically")
    
    print(f"🎯 Access the game at: http://localhost:{port}")


# Create Flask application instance
config_name = get_config_name()
app = create_app(config[config_name])

# Vercel compatibility: Export app for serverless deployment
application = app

if __name__ == '__main__':
    """
    Main entry point when script is run directly.
    
    This starts the Flask development server with configuration based on
    environment variables. In production, use a WSGI server like Gunicorn
    instead of the development server.
    """
    port = get_port()
    debug = config_name == 'development'
    
    print_startup_info(config_name, port, debug)
    
    # Start the development server
    # Note: In production, use a proper WSGI server like Gunicorn
    app.run(
        host='0.0.0.0',  # Listen on all interfaces
        port=port,
        debug=debug,
        threaded=True    # Enable threading for better concurrency
    )
