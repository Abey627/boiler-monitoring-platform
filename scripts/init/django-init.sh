#!/bin/bash

# Django Initialization Script
# This script handles database migrations and other setup tasks

set -e  # Exit on any error

echo "========================================="
echo "Starting Django initialization..."
echo "Service: $DJANGO_SERVICE_NAME"
echo "Settings: $DJANGO_SETTINGS_MODULE"
echo "========================================="

# Wait for database to be ready
echo "Waiting for database connection..."
python manage.py check --database default

# Generate migration files if they don't exist (for development)
if [ "$DEBUG" = "1" ]; then
    echo "Checking for model changes and generating migrations..."
    python manage.py makemigrations --noinput || echo "No new migrations needed"
fi

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Create superuser and demo users if they don't exist (for development)
if [ "$DEBUG" = "1" ]; then
    echo "Setting up development users..."
    
    # Check if demo users should be created
    if [ "$CREATE_DEMO_USERS" = "true" ] && python manage.py help setup_demo_users >/dev/null 2>&1; then
        echo "Creating comprehensive demo user structure..."
        python manage.py setup_demo_users --quiet
    elif python manage.py help create_admin >/dev/null 2>&1; then
        echo "Creating basic admin user..."
        python manage.py create_admin
    else
        # Fallback to standard superuser creation
        echo "Creating fallback superuser..."
        python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@steambytes.com', 'admin123')
    print('Superuser created: admin/admin123')
else:
    print('Superuser already exists')
EOF
    fi
fi

# Collect static files (for services that need it)
if [ -f "manage.py" ] && python manage.py help collectstatic >/dev/null 2>&1; then
    echo "Collecting static files..."
    python manage.py collectstatic --noinput --clear || echo "Static collection skipped or failed"
fi

# Load initial data if fixtures exist
if [ -d "fixtures" ] && [ "$(ls -A fixtures)" ]; then
    echo "Loading initial data fixtures..."
    python manage.py loaddata fixtures/*.json || echo "No fixtures to load or loading failed"
fi

echo "Django initialization completed successfully!"
echo "========================================="

# Start the Django development server
echo "Starting Django development server..."
exec python manage.py runserver 0.0.0.0:${PORT:-8000}
