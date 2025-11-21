# CloudFront Deployment - Final Instructions

## ✅ How It Works Now

The app is configured to **always generate URLs with the proxy prefix** when `APPLICATION_ROOT=/proxy/5000` is set.

### URL Generation:
- **CSS**: `/proxy/5000/static/css/style.css`
- **Links**: `/proxy/5000/about`, `/proxy/5000/game/start`
- **Forms**: Submit to `/proxy/5000/game/guess`, `/proxy/5000/game/reset`

### CloudFront Behavior:
1. User visits: `https://d70ajaldfiod5.cloudfront.net/proxy/5000/`
2. CloudFront strips `/proxy/5000` and forwards to your app: `/`
3. App generates links with `/proxy/5000` prefix
4. CloudFront serves those URLs correctly

## 🚀 Deployment Commands

```bash
cd python

# Set environment variables
export APPLICATION_ROOT=/proxy/5000
export PREFERRED_URL_SCHEME=https
export FLASK_ENV=production
export SECRET_KEY=your-production-secret-key

# Start the application
python app.py
# OR for production:
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🧪 Local Testing

**With proxy config** (to test CloudFront behavior):
```bash
APPLICATION_ROOT=/proxy/5000 python app.py
# Access at: http://localhost:5000/
# Links will include /proxy/5000 prefix
```

**Without proxy config** (normal local development):
```bash
python app.py  
# Access at: http://localhost:5000/
# Links will be normal: /about, /game/start
```

## ✅ What Should Work Now

1. **CSS loads correctly** - `/proxy/5000/static/css/style.css`
2. **All navigation works** - About, Home links include proxy prefix
3. **Game functionality works** - Start game, submit guesses, reset
4. **AJAX works** - Real-time guess feedback without page reload
5. **Play Again button works** - Proper form submission and redirect

## 🔍 Troubleshooting

If links still don't work:
1. Verify `APPLICATION_ROOT=/proxy/5000` is set before starting the app
2. Check that CloudFront is configured to forward headers
3. Ensure CloudFront strips `/proxy/5000` before forwarding to your app

The key insight: **Your app should generate URLs with the proxy prefix, and CloudFront handles the routing.**
