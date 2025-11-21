# Q-Words Python Deployment Guide

## 🚀 Production-Ready Deployment

This guide covers deploying the Q-Words Python application following industry best practices.

## 📋 Prerequisites

- Python 3.8+
- pip package manager
- Virtual environment support
- Web server (for production)

## 🏠 Local Development

### 1. Environment Setup
```bash
# Navigate to project directory
cd qwords-python

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows

# Upgrade pip
pip install --upgrade pip
```

### 2. Install Dependencies
```bash
# Install production dependencies
pip install -r requirements.txt

# For development (includes testing tools)
pip install -r requirements-dev.txt
```

### 3. Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit configuration (use your preferred editor)
nano .env
```

**Minimum .env configuration:**
```env
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production
PORT=5000
WORD_REPOSITORY_TYPE=local
```

### 4. Run Development Server
```bash
# Method 1: Direct execution
python app.py

# Method 2: Flask CLI
export FLASK_APP=app.py
flask run

# Method 3: With specific port
python app.py
```

**Expected Output:**
```
🎮 Starting Q-Words Game Server...
📍 Environment: development
🌐 Port: 5000
🔧 Debug: True
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:5000
 * Running on http://[::1]:5000
```

### 5. Verify Installation
- Open browser to `http://localhost:5000`
- You should see the Q-Words home page
- Try starting a game to verify functionality

## 🌐 Production Deployment

### Option 1: Gunicorn (Recommended)

**1. Install Gunicorn**
```bash
pip install gunicorn
```

**2. Production Configuration**
```bash
# Set environment variables
export FLASK_ENV=production
export SECRET_KEY=your-secure-random-secret-key
export PORT=8000
```

**3. Run with Gunicorn**
```bash
# Basic setup
gunicorn -w 4 -b 0.0.0.0:8000 app:app

# With configuration file
gunicorn -c gunicorn.conf.py app:app

# Background process
gunicorn -w 4 -b 0.0.0.0:8000 app:app --daemon
```

**4. Gunicorn Configuration (gunicorn.conf.py)**
```python
bind = "0.0.0.0:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
preload_app = True
```

### Option 2: Docker Deployment

**1. Build Docker Image**
```bash
docker build -t qwords-python .
```

**2. Run Container**
```bash
# Basic run
docker run -p 8000:8000 qwords-python

# With environment variables
docker run -p 8000:8000 \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-secret-key \
  qwords-python

# Background process
docker run -d -p 8000:8000 --name qwords-app qwords-python
```

**3. Docker Compose (docker-compose.yml)**
```yaml
version: '3.8'
services:
  qwords:
    build: .
    ports:
      - "8000:8000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=your-secret-key
    restart: unless-stopped
```

Run with: `docker-compose up -d`

### Option 3: Cloud Platform Deployment

#### Heroku
```bash
# Install Heroku CLI, then:
heroku login
heroku create your-app-name
git push heroku main

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-secret-key
```

#### AWS Elastic Beanstalk
```bash
# Install EB CLI, then:
eb init
eb create production
eb deploy

# Set environment variables in EB console
```

#### Google Cloud Run
```bash
# Build and deploy
gcloud run deploy qwords \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### DigitalOcean App Platform
```bash
# Create app.yaml
spec:
  name: qwords-python
  services:
  - name: web
    source_dir: /
    github:
      repo: your-username/qwords-python
      branch: main
    run_command: gunicorn --worker-tmp-dir /dev/shm app:app
    environment_slug: python
    instance_count: 1
    instance_size_slug: basic-xxs
    envs:
    - key: FLASK_ENV
      value: production
```

## 🔧 Web Server Configuration

### Nginx (Reverse Proxy)
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static {
        alias /path/to/qwords-python/app/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### Apache (Reverse Proxy)
```apache
<VirtualHost *:80>
    ServerName your-domain.com
    
    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:8000/
    ProxyPassReverse / http://127.0.0.1:8000/
    
    Alias /static /path/to/qwords-python/app/static
    <Directory "/path/to/qwords-python/app/static">
        Require all granted
    </Directory>
</VirtualHost>
```

## 🔒 Security Configuration

### Production Environment Variables
```bash
# Required for production
export FLASK_ENV=production
export SECRET_KEY=your-very-secure-random-secret-key-here
export SESSION_COOKIE_SECURE=true

# Optional security enhancements
export SESSION_COOKIE_HTTPONLY=true
export SESSION_COOKIE_SAMESITE=Lax
```

### SSL/HTTPS Setup
```bash
# With Let's Encrypt (Certbot)
sudo certbot --nginx -d your-domain.com

# Manual certificate
# Update nginx/apache config with SSL settings
```

### Firewall Configuration
```bash
# UFW (Ubuntu)
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable

# Block direct access to app port
sudo ufw deny 8000
```

## 📊 Monitoring & Logging

### Application Logging
```python
# Add to app.py for production logging
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/qwords.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

### Health Checks
```bash
# Basic health check
curl -f http://localhost:8000/game/status || exit 1

# Detailed monitoring
curl -s http://localhost:8000/game/status | jq '.hasActiveGame'
```

### Performance Monitoring
```bash
# Monitor with htop
htop

# Check memory usage
ps aux | grep gunicorn

# Monitor logs
tail -f logs/qwords.log
```

## 🧪 Testing in Production

### Smoke Tests
```bash
# Test home page
curl -I http://your-domain.com/

# Test game start
curl -X POST http://your-domain.com/game/start -d "level=MEDIUM"

# Test game status
curl http://your-domain.com/game/status
```

### Load Testing
```bash
# Install Apache Bench
sudo apt-get install apache2-utils

# Basic load test
ab -n 1000 -c 10 http://your-domain.com/

# Game endpoint test
ab -n 500 -c 5 -p post_data.txt -T application/x-www-form-urlencoded http://your-domain.com/game/start
```

## 🔄 Maintenance

### Updates
```bash
# Pull latest code
git pull origin main

# Update dependencies
pip install -r requirements.txt

# Restart application
sudo systemctl restart qwords  # If using systemd
# OR
docker-compose restart         # If using Docker
```

### Backup
```bash
# Backup application files
tar -czf qwords-backup-$(date +%Y%m%d).tar.gz qwords-python/

# Backup logs
cp logs/qwords.log logs/qwords-backup-$(date +%Y%m%d).log
```

### Database Migration (Future)
```bash
# When migrating to DynamoDB
export WORD_REPOSITORY_TYPE=dynamodb
export AWS_REGION=us-east-1
export DYNAMODB_TABLE_NAME=qwords-words

# Restart application
sudo systemctl restart qwords
```

## 🚨 Troubleshooting

### Common Issues

**Port Already in Use:**
```bash
# Find process using port
sudo lsof -i :8000
# Kill process
sudo kill -9 <PID>
```

**Permission Denied:**
```bash
# Fix file permissions
chmod +x app.py
chown -R www-data:www-data /path/to/qwords-python
```

**Module Not Found:**
```bash
# Verify virtual environment
which python
pip list | grep Flask

# Reinstall dependencies
pip install -r requirements.txt
```

**Memory Issues:**
```bash
# Check memory usage
free -h
# Reduce Gunicorn workers
gunicorn -w 2 -b 0.0.0.0:8000 app:app
```

### Log Analysis
```bash
# Check application logs
tail -f logs/qwords.log

# Check system logs
sudo journalctl -u qwords -f

# Check nginx/apache logs
sudo tail -f /var/log/nginx/error.log
```

## ✅ Deployment Checklist

### Pre-Deployment
- [ ] Code tested locally
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] SSL certificate ready (production)
- [ ] Domain DNS configured
- [ ] Firewall rules set

### Deployment
- [ ] Application deployed
- [ ] Web server configured
- [ ] SSL/HTTPS enabled
- [ ] Health checks passing
- [ ] Monitoring configured
- [ ] Backup strategy implemented

### Post-Deployment
- [ ] Smoke tests completed
- [ ] Performance tests run
- [ ] Monitoring alerts configured
- [ ] Documentation updated
- [ ] Team notified

## 🎯 Performance Optimization

### Application Level
- Use Redis for session storage (high traffic)
- Enable gzip compression
- Implement caching headers
- Optimize static asset delivery

### Infrastructure Level
- Use CDN for static assets
- Implement load balancing
- Set up auto-scaling
- Monitor and optimize database queries

By the lexical archives, your Q-Words application is now ready for production deployment! 🚀

May your vowels be plentiful and your consonants well-placed! ✨
