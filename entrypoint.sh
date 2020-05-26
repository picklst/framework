#!/bin/sh

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Start server
echo "Starting Gunicorn"
gunicorn  framework.wsgi:application \
          --workers=2 \
          --bind=0.0.0.0:8000 \
          --reload
