# Frontend Web Service

Django-based user management and authentication service for the Boiler Monitoring Platform.

## Overview

This service provides:
- User authentication and session management
- Role-based access control
- Organization-based user isolation
- Admin interface for user management
- Audit logging for security compliance

## Quick Start

### Docker (Recommended)
```bash
# From project root
docker-compose up frontend_web
```

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create demo users
python manage.py setup_demo_users

# Run development server
python manage.py runserver
```

## User Roles

- **admin**: Full organization access, user management
- **manager**: Site management, user supervision  
- **operator**: Daily operations, monitoring
- **technician**: Equipment maintenance, technical tasks
- **viewer**: Read-only access, reporting

## API Endpoints

- `/health/` - Health check
- `/api/user-stats/` - User statistics
- `/api/toggle-user-status/` - Toggle user active status

## Demo Users

See [QUICK_START_USER_MANAGEMENT.md](../QUICK_START_USER_MANAGEMENT.md) for complete user list.

## Testing

```bash
# Run tests
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## Environment Variables

- `DEBUG` - Enable debug mode (default: 1)
- `SECRET_KEY` - Django secret key
- `DB_PASSWORD` - PostgreSQL password
- `CREATE_DEMO_USERS` - Create demo users on startup (default: true)

## Database Models

- **Organization** - Client companies using the platform
- **User** - Extended Django user with roles and organization
- **UserProfile** - User preferences and settings
- **AuditLog** - Security and compliance logging
