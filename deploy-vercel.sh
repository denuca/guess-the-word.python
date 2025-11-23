#!/bin/bash

# Guess The Word Vercel Deployment Script
# Automates the deployment process to Vercel

set -e  # Exit on any error

echo "🚀 Guess The Word Vercel Deployment Script"
echo "===================================="

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Please run this script from the python/ directory."
    exit 1
fi

# Check if vercel.json exists
if [ ! -f "vercel.json" ]; then
    echo "❌ Error: vercel.json not found. Please ensure Vercel configuration exists."
    exit 1
fi

echo "✅ Pre-flight checks passed"

# Login to Vercel (if not already logged in)
echo "🔐 Checking Vercel authentication..."
if ! vercel whoami &> /dev/null; then
    echo "Please login to Vercel:"
    vercel login
fi

echo "✅ Authenticated with Vercel"

# Set production environment variables
echo "⚙️  Setting up environment variables..."

# Generate secure secret key if not exists
if ! vercel env ls | grep -q "SECRET_KEY"; then
    echo "🔑 Generating secure SECRET_KEY..."
    SECRET_KEY=$(openssl rand -base64 32)
    echo "$SECRET_KEY" | vercel env add SECRET_KEY production
fi

# Set Flask environment
echo "production" | vercel env add FLASK_ENV production --force

# Set HTTPS scheme
echo "https" | vercel env add PREFERRED_URL_SCHEME production --force

# Set secure cookies
echo "true" | vercel env add SESSION_COOKIE_SECURE production --force

echo "✅ Environment variables configured"

# Deploy to production
echo "🚀 Deploying to Vercel..."
vercel --prod --confirm

echo ""
echo "🎉 Deployment completed successfully!"
echo ""
echo "📋 Next steps:"
echo "1. Test your deployment URL"
echo "2. Verify accessibility features work"
echo "3. Check mobile responsiveness"
echo "4. Test keyboard navigation"
echo ""
echo "🔗 Useful commands:"
echo "  vercel logs           - View deployment logs"
echo "  vercel domains        - Manage custom domains"
echo "  vercel env            - Manage environment variables"
echo ""
echo "✨ Your accessible Guess The Word game is now live!"
