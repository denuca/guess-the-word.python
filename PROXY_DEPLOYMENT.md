# Guess The Word Proxy Deployment Guide

## Issue: CloudFront Proxy URL Problems

When deploying behind a CloudFront proxy with URLs like `https://d70ajaldfiod5.cloudfront.net/proxy/5000/`, Flask needs special configuration to handle the proxy prefix correctly.

## Quick Fix

Set these environment variables before starting the application:

```bash
export APPLICATION_ROOT=/proxy/5000
export PREFERRED_URL_SCHEME=https
export FLASK_ENV=production
export SECRET_KEY=your-production-secret-key

# Then start the app
python app.py
# OR
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Using the Deployment Config File

```bash
# Load proxy configuration
source deploy-proxy.env

# Start the application
python app.py
```

## Environment Variables Explained

| Variable | Purpose | Example |
|----------|---------|---------|
| `APPLICATION_ROOT` | Proxy path prefix | `/proxy/5000` |
| `PREFERRED_URL_SCHEME` | URL scheme behind proxy | `https` |
| `FLASK_ENV` | Environment mode | `production` |
| `SECRET_KEY` | Session encryption | `your-secret-key` |

## How It Works

1. **ProxyFix Middleware**: Handles `X-Forwarded-*` headers from CloudFront
2. **APPLICATION_ROOT**: Tells Flask about the proxy path prefix
3. **PREFERRED_URL_SCHEME**: Ensures HTTPS URLs are generated
4. **url_for()**: All redirects use Flask's `url_for()` which respects proxy settings

## Testing Proxy Configuration

```python
# Test URL generation with proxy settings
import os
os.environ['APPLICATION_ROOT'] = '/proxy/5000'
os.environ['PREFERRED_URL_SCHEME'] = 'https'

from app import create_app
from config.settings import ProductionConfig

app = create_app(ProductionConfig)
with app.app_context():
    from flask import url_for
    print(url_for('home.index'))        # Should include proxy prefix
    print(url_for('game.game_page'))    # Should include proxy prefix
    print(url_for('static', filename='css/style.css'))  # Should include proxy prefix
```

## CSS Loading Issues

If CSS isn't loading, check:

1. **Static file URLs**: Should include proxy prefix
2. **Content-Type headers**: CloudFront should serve CSS with correct MIME type
3. **Cache headers**: CloudFront might be caching old responses

### Force CSS Reload

Add version parameter to CSS link:

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}?v=1">
```

## CloudFront Configuration

Ensure CloudFront forwards these headers:
- `X-Forwarded-For`
- `X-Forwarded-Proto`
- `X-Forwarded-Host`
- `X-Forwarded-Prefix`

## Troubleshooting

### Problem: Redirects go to wrong URL
**Solution**: Set `APPLICATION_ROOT` environment variable

### Problem: CSS not loading
**Solution**: Check static file URL generation and CloudFront MIME types

### Problem: HTTPS mixed content warnings
**Solution**: Set `PREFERRED_URL_SCHEME=https`

### Problem: Session cookies not working
**Solution**: Set `SESSION_COOKIE_SECURE=true` for HTTPS

## Complete Deployment Command

```bash
# Set all required environment variables
export FLASK_ENV=production
export SECRET_KEY=your-production-secret-key-here
export APPLICATION_ROOT=/proxy/5000
export PREFERRED_URL_SCHEME=https
export SESSION_COOKIE_SECURE=true

# Start with Gunicorn (recommended for production)
gunicorn -w 4 -b 0.0.0.0:5000 --access-logfile - --error-logfile - app:app
```

This configuration ensures:
- ✅ Correct URL generation with proxy prefix
- ✅ HTTPS URLs for all links and redirects
- ✅ Secure session cookies
- ✅ Static files (CSS/JS) load correctly
- ✅ Form submissions redirect to correct URLs
