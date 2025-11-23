"""
Vercel serverless function entry point for Guess The Word application.

This module provides the WSGI application interface required by Vercel
for deploying Flask applications as serverless functions.
"""

import sys
import os

# Add the parent directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app
from config.settings import ProductionConfig

# Create the Flask application instance
app = create_app(ProductionConfig)

# Vercel expects the WSGI application to be named 'app'
# This is the entry point for the serverless function
if __name__ == "__main__":
    app.run()
