#!/usr/bin/env python3
"""
Test script to verify proxy configuration is working
"""

import os

# IMPORTANT: Set environment variables BEFORE importing Flask
os.environ['APPLICATION_ROOT'] = '/proxy/5000'
os.environ['PREFERRED_URL_SCHEME'] = 'https'
os.environ['FLASK_ENV'] = 'production'

from app import create_app
from config.settings import DevelopmentConfig

print("🧪 Testing Proxy Configuration")
print("=" * 50)

app = create_app(DevelopmentConfig)

with app.test_client() as client:
    # Test home page URLs
    response = client.get('/')
    html = response.data.decode()
    
    print("✅ Home page links:")
    import re
    hrefs = re.findall(r'href="([^"]+)"', html)
    for href in hrefs:
        if '/proxy/5000' in href:
            print(f"  ✅ {href}")
        else:
            print(f"  ❌ {href}")
    
    # Test form submission
    response = client.post('/game/start', data={'level': 'MEDIUM'})
    redirect_url = response.headers.get('Location', 'No redirect')
    
    print(f"\n✅ Form redirect:")
    if '/proxy/5000' in redirect_url:
        print(f"  ✅ {redirect_url}")
    else:
        print(f"  ❌ {redirect_url}")

print("\n🚀 To run with proxy config:")
print("APPLICATION_ROOT=/proxy/5000 PREFERRED_URL_SCHEME=https python app.py")
