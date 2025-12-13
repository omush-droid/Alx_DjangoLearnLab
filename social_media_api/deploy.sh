#!/bin/bash

# Deployment script for production

echo "Starting deployment..."

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate

# Create superuser if needed (optional)
# python manage.py createsuperuser --noinput

echo "Deployment completed successfully!"