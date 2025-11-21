#!/bin/bash
# Start Q-Words with proxy configuration

cd "$(dirname "$0")"
source venv/bin/activate

export APPLICATION_ROOT=/proxy/5000
export PREFERRED_URL_SCHEME=https
export FLASK_ENV=production
export SECRET_KEY=${SECRET_KEY:-dev-secret-key}

echo "🚀 Starting Q-Words with proxy configuration..."
echo "   APPLICATION_ROOT: $APPLICATION_ROOT"
echo "   PREFERRED_URL_SCHEME: $PREFERRED_URL_SCHEME"
echo ""
echo "🌐 For local testing, access at:"
echo "   http://localhost:5000/ (without proxy prefix)"
echo ""
echo "🌐 For CloudFront deployment, URLs will be:"
echo "   https://d70ajaldfiod5.cloudfront.net/proxy/5000/"
echo ""

python app.py
