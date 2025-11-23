# Guess The Word Vercel Deployment Guide

## 🚀 Deploy to Vercel

Deploy the Guess The Word accessible word-guessing game to Vercel in minutes with serverless functions.

### Prerequisites

- [Vercel CLI](https://vercel.com/cli) installed
- Git repository (GitHub, GitLab, or Bitbucket)
- Vercel account (free tier available)

## 📋 Quick Deployment

### Method 1: Vercel CLI (Recommended)

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy from project directory**:
   ```bash
   cd python
   vercel --prod
   ```

4. **Follow prompts**:
   - Set up and deploy? `Y`
   - Which scope? Select your account
   - Link to existing project? `N`
   - Project name: `qwords-game` (or your choice)
   - Directory: `./` (current directory)

### Method 2: Git Integration

1. **Push to Git repository**:
   ```bash
   git add .
   git commit -m "Add Guess The Word Flask app"
   git push origin main
   ```

2. **Import on Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your Git repository
   - Vercel auto-detects Python and deploys

## ⚙️ Configuration Files

### `vercel.json`
```json
{
  "version": 2,
  "builds": [
    {
      "src": "app.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/static/$1"
    },
    {
      "src": "/(.*)",
      "dest": "/app.py"
    }
  ]
}
```

### Environment Variables

Set these in Vercel dashboard or CLI:

```bash
# Production environment
vercel env add FLASK_ENV production
vercel env add SECRET_KEY your-secret-key-here
vercel env add PREFERRED_URL_SCHEME https
```

## 🔧 Project Structure for Vercel

```
python/
├── api/
│   └── index.py          # Vercel serverless entry point
├── app/                  # Flask application
├── config/               # Configuration
├── static/               # CSS, JS, images
├── templates/            # HTML templates
├── app.py               # Main application (Vercel compatible)
├── requirements.txt     # Python dependencies
├── vercel.json         # Vercel configuration
└── VERCEL_DEPLOYMENT.md # This file
```

## 🌐 Custom Domain (Optional)

1. **Add domain in Vercel dashboard**:
   - Go to Project Settings → Domains
   - Add your custom domain
   - Follow DNS configuration instructions

2. **Update environment variables**:
   ```bash
   vercel env add PREFERRED_URL_SCHEME https
   ```

## 📊 Monitoring & Analytics

Vercel provides built-in:
- **Performance monitoring**
- **Error tracking**
- **Analytics dashboard**
- **Function logs**

Access via: Project Dashboard → Functions/Analytics tabs

## 🔍 Troubleshooting

### Common Issues

**Build Fails**:
```bash
# Check Python version compatibility
python --version  # Should be 3.8+

# Verify requirements.txt
pip install -r requirements.txt
```

**Static Files Not Loading**:
- Ensure `vercel.json` routes are configured
- Check static file paths in templates
- Verify CSS/JS files are in `/static/` directory

**Session Issues**:
```bash
# Set secure session configuration
vercel env add SESSION_COOKIE_SECURE true
vercel env add SECRET_KEY $(openssl rand -base64 32)
```

**Function Timeout**:
- Vercel free tier: 10s limit
- Pro tier: 60s limit
- Optimize slow operations

### Debug Deployment

```bash
# View deployment logs
vercel logs

# Check function logs
vercel logs --follow

# Test locally with Vercel dev
vercel dev
```

## 🚀 Production Checklist

- [ ] Set `FLASK_ENV=production`
- [ ] Configure secure `SECRET_KEY`
- [ ] Enable HTTPS with `PREFERRED_URL_SCHEME=https`
- [ ] Set `SESSION_COOKIE_SECURE=true`
- [ ] Test all game functionality
- [ ] Verify accessibility features work
- [ ] Check mobile responsiveness
- [ ] Test keyboard navigation
- [ ] Validate WCAG compliance

## 📈 Performance Optimization

### Vercel-Specific Optimizations

1. **Static Asset Caching**:
   ```json
   {
     "headers": [
       {
         "source": "/static/(.*)",
         "headers": [
           {
             "key": "Cache-Control",
             "value": "public, max-age=31536000, immutable"
           }
         ]
       }
     ]
   }
   ```

2. **Function Configuration**:
   ```json
   {
     "functions": {
       "app.py": {
         "maxDuration": 10,
         "memory": 1024
       }
     }
   }
   ```

## 🔒 Security Configuration

### Environment Variables

```bash
# Required for production
vercel env add SECRET_KEY $(openssl rand -base64 32)
vercel env add FLASK_ENV production
vercel env add SESSION_COOKIE_SECURE true
vercel env add PREFERRED_URL_SCHEME https

# Optional security headers
vercel env add FORCE_HTTPS true
```

### Security Headers

Add to `vercel.json`:
```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        },
        {
          "key": "X-XSS-Protection",
          "value": "1; mode=block"
        }
      ]
    }
  ]
}
```

## 📱 Testing Deployment

### Accessibility Testing

After deployment, test:
- **Screen readers**: NVDA, JAWS, VoiceOver
- **Keyboard navigation**: Tab, Arrow keys, Enter/Space
- **Mobile accessibility**: iOS VoiceOver, Android TalkBack
- **High contrast mode**: Windows/macOS high contrast
- **Zoom functionality**: 200% browser zoom

### Performance Testing

```bash
# Lighthouse audit
npx lighthouse https://your-app.vercel.app --view

# WebPageTest
# Visit webpagetest.org with your Vercel URL
```

## 🎯 Example Deployment

**Live Demo**: `https://qwords-game.vercel.app`

**Features Verified**:
- ✅ WCAG 2.1 AA compliance
- ✅ Full keyboard navigation
- ✅ Mobile responsive design
- ✅ Screen reader compatibility
- ✅ Fast serverless performance
- ✅ Global CDN distribution

## 📞 Support

- **Vercel Documentation**: [vercel.com/docs](https://vercel.com/docs)
- **Flask on Vercel**: [vercel.com/guides/using-flask-with-vercel](https://vercel.com/guides/using-flask-with-vercel)
- **Guess The Word Issues**: Create issue in project repository

---

**Ready to deploy?** Run `vercel --prod` and share your accessible word game with the world! 🌍✨
