# Social Media API - Production Deployment Guide

This guide covers deploying the Social Media API to various production environments.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Git
- PostgreSQL (for production)
- Domain name (optional but recommended)

### Environment Variables
Copy `.env.example` to `.env` and configure:
```bash
cp .env.example .env
```

Required variables:
- `SECRET_KEY`: Django secret key (generate new for production)
- `DEBUG`: Set to `False` for production
- `ALLOWED_HOSTS`: Your domain names and IPs
- `DATABASE_URL`: PostgreSQL connection string
- `SECURE_SSL_REDIRECT`: Set to `True` for HTTPS

## 📋 Deployment Options

### 1. Heroku Deployment (Recommended for beginners)

#### Prerequisites
- Heroku CLI installed
- Git repository

#### Steps
1. **Run the deployment script:**
   ```bash
   chmod +x deploy_heroku.sh
   ./deploy_heroku.sh
   ```

2. **Manual deployment (alternative):**
   ```bash
   # Login to Heroku
   heroku login
   
   # Create app
   heroku create your-app-name
   
   # Set environment variables
   heroku config:set DEBUG=False
   heroku config:set SECRET_KEY=your-secret-key
   heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com
   
   # Add PostgreSQL
   heroku addons:create heroku-postgresql:mini
   
   # Deploy
   git push heroku main
   
   # Run migrations
   heroku run python manage.py migrate
   ```

#### Heroku Configuration Files
- `Procfile`: Defines how to run the app
- `runtime.txt`: Specifies Python version
- `requirements.txt`: Python dependencies

### 2. DigitalOcean Droplet Deployment

#### Prerequisites
- DigitalOcean droplet (Ubuntu 20.04+)
- Domain name pointed to droplet IP
- SSH access to droplet

#### Steps
1. **Connect to your droplet:**
   ```bash
   ssh root@your-droplet-ip
   ```

2. **Run the deployment script:**
   ```bash
   wget https://raw.githubusercontent.com/yourusername/social_media_api/main/deploy_digitalocean.sh
   chmod +x deploy_digitalocean.sh
   ./deploy_digitalocean.sh
   ```

3. **Update configuration:**
   - Edit `/etc/nginx/sites-available/social_media_api`
   - Update domain names
   - Configure SSL with Let's Encrypt

### 3. Docker Deployment

#### Prerequisites
- Docker and Docker Compose installed

#### Steps
1. **Build and run with Docker Compose:**
   ```bash
   # Build images
   docker-compose build
   
   # Start services
   docker-compose up -d
   
   # Run migrations
   docker-compose exec web python manage.py migrate
   
   # Create superuser
   docker-compose exec web python manage.py createsuperuser
   ```

2. **Production Docker setup:**
   ```bash
   # Use production environment file
   cp .env.example .env.production
   # Edit .env.production with production values
   
   # Run with production settings
   docker-compose -f docker-compose.yml --env-file .env.production up -d
   ```

### 4. AWS Elastic Beanstalk Deployment

#### Prerequisites
- AWS CLI configured
- EB CLI installed

#### Steps
1. **Initialize Elastic Beanstalk:**
   ```bash
   eb init
   ```

2. **Create environment:**
   ```bash
   eb create production
   ```

3. **Set environment variables:**
   ```bash
   eb setenv DEBUG=False SECRET_KEY=your-secret-key ALLOWED_HOSTS=your-app.region.elasticbeanstalk.com
   ```

4. **Deploy:**
   ```bash
   eb deploy
   ```

## 🔧 Configuration Details

### Security Settings
The following security settings are automatically applied in production:

```python
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True  # When HTTPS is available
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Static Files
- Uses WhiteNoise for static file serving
- Automatically compresses and caches static files
- Collects static files during deployment

### Database
- Development: SQLite
- Production: PostgreSQL (recommended)
- Supports DATABASE_URL environment variable

### Logging
- Console logging for INFO level and above
- File logging for ERROR level
- Structured logging with timestamps and module information

## 📊 Monitoring and Maintenance

### Health Checks
Create a simple health check endpoint:

```python
# In your main urls.py
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def health_check(request):
    return JsonResponse({"status": "healthy"})

urlpatterns = [
    # ... other patterns
    path('health/', health_check, name='health_check'),
]
```

### Monitoring Tools
- **Heroku**: Built-in metrics and logging
- **DigitalOcean**: Use monitoring add-ons
- **AWS**: CloudWatch integration
- **External**: Consider Sentry for error tracking

### Backup Strategy
1. **Database backups:**
   ```bash
   # Heroku
   heroku pg:backups:capture
   
   # PostgreSQL
   pg_dump social_media_db > backup.sql
   ```

2. **Media files backup:**
   - Use cloud storage (AWS S3, DigitalOcean Spaces)
   - Regular automated backups

### Updates and Maintenance
1. **Regular updates:**
   ```bash
   # Update dependencies
   pip install -r requirements.txt --upgrade
   
   # Run migrations
   python manage.py migrate
   
   # Collect static files
   python manage.py collectstatic --noinput
   ```

2. **Zero-downtime deployments:**
   - Use blue-green deployment strategy
   - Database migrations should be backward compatible

## 🔍 Troubleshooting

### Common Issues

1. **Static files not loading:**
   ```bash
   python manage.py collectstatic --noinput
   ```

2. **Database connection errors:**
   - Check DATABASE_URL format
   - Verify database credentials
   - Ensure database server is running

3. **Permission errors:**
   ```bash
   # Fix file permissions
   chmod -R 755 /var/www/social_media_api
   chown -R www-data:www-data /var/www/social_media_api
   ```

4. **SSL certificate issues:**
   ```bash
   # Renew Let's Encrypt certificate
   sudo certbot renew
   ```

### Logs and Debugging
```bash
# Heroku logs
heroku logs --tail

# DigitalOcean/Ubuntu logs
sudo journalctl -u social_media_api -f
sudo tail -f /var/log/nginx/error.log

# Docker logs
docker-compose logs -f web
```

## 📝 Post-Deployment Checklist

- [ ] Environment variables configured
- [ ] Database migrations applied
- [ ] Static files collected and serving
- [ ] SSL certificate installed (if applicable)
- [ ] Domain name configured
- [ ] Admin user created
- [ ] API endpoints tested
- [ ] Monitoring and logging configured
- [ ] Backup strategy implemented
- [ ] Documentation updated with live URLs

## 🌐 Live URLs

After deployment, your API will be available at:
- **Heroku**: `https://your-app-name.herokuapp.com`
- **DigitalOcean**: `https://your-domain.com`
- **Docker**: `http://localhost` (or your server IP)
- **AWS EB**: `https://your-app.region.elasticbeanstalk.com`

### API Endpoints
- Admin: `/admin/`
- API Root: `/api/`
- Authentication: `/api/accounts/`
- Posts: `/api/posts/`
- Comments: `/api/comments/`
- Feed: `/api/feed/`
- Notifications: `/api/notifications/`

## 📞 Support

For deployment issues:
1. Check the troubleshooting section
2. Review platform-specific documentation
3. Check application logs
4. Verify environment variables
5. Test database connectivity

Remember to keep your secret keys secure and never commit them to version control!