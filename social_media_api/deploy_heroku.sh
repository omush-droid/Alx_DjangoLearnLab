#!/bin/bash

# Heroku Deployment Script for Social Media API

echo "🚀 Starting Heroku deployment..."

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI not found. Please install it first."
    exit 1
fi

# Login to Heroku (if not already logged in)
echo "📝 Checking Heroku authentication..."
heroku auth:whoami || heroku login

# Create Heroku app (replace 'your-app-name' with your desired app name)
read -p "Enter your Heroku app name: " APP_NAME
heroku create $APP_NAME

# Set environment variables
echo "🔧 Setting environment variables..."
heroku config:set DEBUG=False --app $APP_NAME
heroku config:set SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())') --app $APP_NAME
heroku config:set ALLOWED_HOSTS=$APP_NAME.herokuapp.com --app $APP_NAME
heroku config:set SECURE_SSL_REDIRECT=True --app $APP_NAME

# Add PostgreSQL addon
echo "🗄️ Adding PostgreSQL database..."
heroku addons:create heroku-postgresql:mini --app $APP_NAME

# Deploy to Heroku
echo "📦 Deploying to Heroku..."
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Run migrations
echo "🔄 Running database migrations..."
heroku run python manage.py migrate --app $APP_NAME

# Create superuser (optional)
read -p "Do you want to create a superuser? (y/n): " CREATE_SUPERUSER
if [ "$CREATE_SUPERUSER" = "y" ]; then
    heroku run python manage.py createsuperuser --app $APP_NAME
fi

echo "✅ Deployment complete!"
echo "🌐 Your app is available at: https://$APP_NAME.herokuapp.com"
echo "🔧 Admin panel: https://$APP_NAME.herokuapp.com/admin/"