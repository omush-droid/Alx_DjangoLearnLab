#!/bin/bash

# DigitalOcean Deployment Script for Social Media API

echo "🚀 Starting DigitalOcean deployment setup..."

# Update system packages
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install required packages
echo "🔧 Installing required packages..."
sudo apt install -y python3-pip python3-venv nginx postgresql postgresql-contrib supervisor git

# Create application directory
APP_DIR="/var/www/social_media_api"
sudo mkdir -p $APP_DIR
sudo chown $USER:$USER $APP_DIR

# Clone repository (replace with your repository URL)
echo "📥 Cloning repository..."
cd /var/www
git clone https://github.com/yourusername/social_media_api.git
cd social_media_api

# Create virtual environment
echo "🐍 Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Set up PostgreSQL database
echo "🗄️ Setting up PostgreSQL database..."
sudo -u postgres createdb social_media_db
sudo -u postgres createuser social_media_user
sudo -u postgres psql -c "ALTER USER social_media_user WITH PASSWORD 'your_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE social_media_db TO social_media_user;"

# Create .env file
echo "📝 Creating environment file..."
cat > .env << EOF
SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com,your-server-ip
DATABASE_URL=postgres://social_media_user:your_password@localhost:5432/social_media_db
SECURE_SSL_REDIRECT=True
EOF

# Run Django setup
echo "🔄 Running Django setup..."
python manage.py collectstatic --noinput
python manage.py migrate

# Create Gunicorn systemd service
echo "⚙️ Setting up Gunicorn service..."
sudo tee /etc/systemd/system/social_media_api.service > /dev/null << EOF
[Unit]
Description=Social Media API Gunicorn daemon
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=$APP_DIR
ExecStart=$APP_DIR/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:$APP_DIR/social_media_api.sock social_media_api.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

# Start and enable Gunicorn service
sudo systemctl start social_media_api
sudo systemctl enable social_media_api

# Configure Nginx
echo "🌐 Configuring Nginx..."
sudo tee /etc/nginx/sites-available/social_media_api > /dev/null << EOF
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root $APP_DIR;
    }
    
    location /media/ {
        root $APP_DIR;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:$APP_DIR/social_media_api.sock;
    }
}
EOF

# Enable Nginx site
sudo ln -s /etc/nginx/sites-available/social_media_api /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx

# Set up SSL with Let's Encrypt (optional)
echo "🔒 Setting up SSL certificate..."
sudo apt install -y certbot python3-certbot-nginx
# sudo certbot --nginx -d your-domain.com -d www.your-domain.com

echo "✅ Deployment setup complete!"
echo "🌐 Your app should be available at: http://your-domain.com"
echo "📝 Don't forget to:"
echo "   1. Update your domain name in the Nginx config"
echo "   2. Update ALLOWED_HOSTS in .env"
echo "   3. Run SSL certificate setup: sudo certbot --nginx -d your-domain.com"