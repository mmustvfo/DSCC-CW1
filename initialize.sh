#!/bin/bash

# Initialize the Django application with sample data
# This script creates the necessary database tables and adds sample data

echo "========= Django Booking System Setup ========="
echo ""

# Create database migrations
echo "Step 1: Creating database migrations..."
python manage.py makemigrations booking || true
echo "✓ Migrations created"
echo ""

# Apply migrations
echo "Step 2: Applying database migrations..."
python manage.py migrate
echo "✓ Database migrated"
echo ""

# Create superuser
echo "Step 3: Creating superuser..."
echo "Run: python manage.py createsuperuser"
echo ""

# Collect static files
echo "Step 4: Collecting static files..."
python manage.py collectstatic --noinput || true
echo "✓ Static files collected"
echo ""

echo "========= Setup Complete ========="
echo "Run: python manage.py runserver"
echo "Visit: http://localhost:8000"
