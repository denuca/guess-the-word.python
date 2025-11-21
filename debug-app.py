#!/usr/bin/env python3
import os
os.environ['APPLICATION_ROOT'] = '/proxy/5000'
os.environ['PREFERRED_URL_SCHEME'] = 'https'

from app import create_app
from config.settings import DevelopmentConfig

app = create_app(DevelopmentConfig)

@app.route('/debug')
def debug():
    from flask import url_for
    return f"""
    <h1>Debug Info</h1>
    <p>APPLICATION_ROOT: {app.config.get('APPLICATION_ROOT')}</p>
    <p>PREFERRED_URL_SCHEME: {app.config.get('PREFERRED_URL_SCHEME')}</p>
    <p>Home URL: {url_for('home.index')}</p>
    <p>About URL: {url_for('home.about')}</p>
    <p>CSS URL: {url_for('static', filename='css/style.css')}</p>
    """

if __name__ == '__main__':
    print("Debug app starting...")
    app.run(host='0.0.0.0', port=5001, debug=True)
