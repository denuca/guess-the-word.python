#!/bin/bash
# Q-Words Proxy Deployment Script
# Configures environment for CloudFront proxy deployment

echo "🚀 Q-Words Proxy Deployment Setup"
echo "=================================="

# Set proxy environment variables
export FLASK_ENV=production
export APPLICATION_ROOT=/proxy/5000
export PREFERRED_URL_SCHEME=https
export SESSION_COOKIE_SECURE=true
export WORD_REPOSITORY_TYPE=local

# Prompt for secret key if not set
if [ -z "$SECRET_KEY" ]; then
    echo "⚠️  SECRET_KEY not set. Please set it:"
    echo "   export SECRET_KEY=your-production-secret-key"
    echo ""
fi

echo "✅ Environment configured for proxy deployment:"
echo "   APPLICATION_ROOT: $APPLICATION_ROOT"
echo "   PREFERRED_URL_SCHEME: $PREFERRED_URL_SCHEME"
echo "   FLASK_ENV: $FLASK_ENV"
echo ""

echo "🎯 Start the application with:"
echo "   gunicorn -w 4 -b 0.0.0.0:5000 app:app"
echo ""
echo "🌐 Access via CloudFront:"
echo "   https://d70ajaldfiod5.cloudfront.net/proxy/5000/"
