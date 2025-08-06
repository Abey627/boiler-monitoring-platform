#!/bin/bash

# Demo User Setup Script
# This script sets up comprehensive demo users for the boiler monitoring platform
# Can be run independently or as part of the Docker initialization

set -e

echo "========================================="
echo "Setting up demo users for Boiler Monitoring Platform"
echo "========================================="

# Navigate to the frontend_web directory
cd "$(dirname "$0")/../frontend_web"

# Check if we're in a Docker container or local environment
if [ -f "/.dockerenv" ] || [ "$CONTAINER" = "true" ]; then
    echo "Running in Docker container..."
    DB_CHECK_CMD="python manage.py check --database default"
else
    echo "Running in local environment..."
    DB_CHECK_CMD="python manage.py check --database default"
fi

# Wait for database to be ready
echo "Checking database connection..."
$DB_CHECK_CMD

# Apply any pending migrations first
echo "Applying migrations..."
python manage.py migrate --noinput

# Set up demo users
echo "Creating demo users and organizations..."
python manage.py setup_demo_users

echo "========================================="
echo "Demo user setup completed!"
echo ""
echo "You can now access:"
echo "  🌐 Web Dashboard: http://localhost:8000/"
echo "  ⚙️  Admin Panel: http://localhost:8000/admin/"
echo ""
echo "Platform Superusers (password: admin123):"
echo "  • ceo - CEO/Executive level access"
echo "  • head_operations - Head of Operations"  
echo "  • dev_lead - Development Team Lead"
echo ""
echo "Platform Operators (password: operator123):"
echo "  • platform_admin - Platform administrator"
echo "  • platform_operator - Platform operations"
echo ""
echo "Organization Users:"
echo "  ACME Corporation (password: acme123):"
echo "    • acme_admin, acme_manager, acme_operator1, acme_operator2, acme_tech, acme_viewer"
echo ""
echo "  Tech Solutions Inc (password: tech123):"
echo "    • tech_admin, tech_manager, tech_operator1, tech_operator2, tech_specialist"
echo ""
echo "========================================="
