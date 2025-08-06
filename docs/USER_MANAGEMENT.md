# User Management Implementation Guide

## Overview

This implementation provides a comprehensive user management system for the Boiler Monitoring Platform with support for:

1. **Platform Superusers** - Developer team, Head of Department, CEO
2. **Platform Operators** - Operation team to manage clients (organizations)  
3. **Organization Users** - Multiple organizations with multiple sites and users

## User Hierarchy

### 1. Platform Level Users (No Organization)

#### Superusers (password: `admin123`)
- `ceo` - CEO/Executive level access
- `head_operations` - Head of Operations  
- `dev_lead` - Development Team Lead

#### Platform Operators (password: `operator123`)
- `platform_admin` - Platform administrator
- `platform_operator` - Platform operations manager

### 2. Organization Level Users

#### ACME Corporation (password: `acme123`)
- `acme_admin` - Organization administrator
- `acme_manager` - Site manager
- `acme_operator1` - Plant A operator
- `acme_operator2` - Plant B operator
- `acme_tech` - Maintenance technician
- `acme_viewer` - Reporting & analytics viewer

#### Tech Solutions Inc (password: `tech123`)
- `tech_admin` - IT Operations administrator
- `tech_manager` - Data Center manager
- `tech_operator1` - Server Farm Alpha operator
- `tech_operator2` - Server Farm Beta operator
- `tech_specialist` - Systems engineer

## User Roles & Permissions

| Role | Permissions |
|------|-------------|
| `admin` | Full organization access, user management |
| `manager` | Site management, user supervision |
| `operator` | Daily operations, monitoring |
| `technician` | Equipment maintenance, technical tasks |
| `viewer` | Read-only access, reporting |

## Quick Setup

### Option 1: Docker Compose (Recommended)

The demo users are automatically created when you start the frontend_web service:

```bash
docker-compose up frontend_web
```

The `CREATE_DEMO_USERS=true` environment variable in docker-compose.yml enables automatic demo user creation.

### Option 2: Manual Setup Scripts

#### Windows (PowerShell)
```powershell
.\scripts\setup_demo_users.ps1
```

#### Linux/Mac (Bash)
```bash
./scripts/setup_demo_users.sh
```

### Option 3: Django Management Commands

```bash
# Navigate to frontend_web directory
cd frontend_web

# Create comprehensive demo users
python manage.py setup_demo_users

# Or create just basic admin user
python manage.py create_admin

# Reset and recreate demo users
python manage.py setup_demo_users --reset
```

## Access Points

- **Web Dashboard**: http://localhost:8000/
- **Admin Panel**: http://localhost:8000/admin/
- **Health Check**: http://localhost:8000/health/

## Database Models

### Organization
- Represents client companies using the platform
- Each organization can have multiple users and sites
- Fields: name, code, contact_email, phone, address, is_active

### User (Custom Django User)
- Extended user model with role-based access control
- Belongs to an organization (except platform users)
- Fields: organization, role, phone, department, last_login_ip

### UserProfile
- Additional user preferences and settings
- One-to-one relationship with User
- Fields: timezone, language, theme, notification preferences

### AuditLog
- Tracks all user actions and system events
- Important for compliance and security monitoring
- Fields: user, action, target_user, timestamp, ip_address, details

## Features

### ✅ Implemented
- Complete user hierarchy with demo data
- Role-based access control
- User authentication and session management
- Basic dashboard with user statistics
- Admin panel with comprehensive user management
- Audit logging for security tracking
- User profile management
- Organization-based user isolation

### 🚧 In Development
- Advanced user creation/editing forms
- Site management within organizations
- Real-time monitoring dashboard
- Alert management system
- User invitation system

### 📋 Planned
- LDAP/Active Directory integration
- Multi-factor authentication
- API key management
- Advanced reporting and analytics
- Mobile app authentication

## Configuration

### Environment Variables

```bash
# Enable demo user creation (in docker-compose.yml)
CREATE_DEMO_USERS=true

# Database settings
POSTGRES_DB=steambytes_core
POSTGRES_USER=steambytes
DB_PASSWORD=steambytes_dev_password

# Django settings
DEBUG=1
SECRET_KEY=your-secret-key
```

### Settings (frontend_web/settings.py)

```python
# Custom user model
AUTH_USER_MODEL = 'dashboard.User'

# Login/logout URLs
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'
```

## Security Features

1. **Password Validation** - Django's built-in password validators
2. **Session Management** - Redis-backed sessions in production
3. **Audit Logging** - All user actions tracked
4. **IP Tracking** - Last login IP recorded
5. **Role-based Access** - Granular permission system
6. **CSRF Protection** - Django's CSRF middleware
7. **Secure Headers** - Security middleware enabled

## Troubleshooting

### Common Issues

1. **Migration Errors**
   ```bash
   python manage.py makemigrations dashboard
   python manage.py migrate
   ```

2. **Demo Users Not Created**
   - Check `CREATE_DEMO_USERS=true` in docker-compose.yml
   - Run manually: `python manage.py setup_demo_users`

3. **Database Connection Issues**
   - Ensure PostgreSQL is running
   - Check database credentials in .env file

4. **Permission Denied**
   - Check user roles and organization membership
   - Verify is_active status

### Reset Demo Data

```bash
# Reset and recreate all demo users
python manage.py setup_demo_users --reset

# Or manually delete from admin panel
```

## Development Notes

- The implementation focuses on clean, scalable code
- Uses Django's built-in authentication with custom extensions
- Follows microservice-ready patterns
- Includes comprehensive logging and audit trails
- Ready for horizontal scaling with Redis sessions

## Next Steps

1. Test the implementation with `docker-compose up`
2. Access http://localhost:8000/ and try different user logins
3. Explore the admin panel at http://localhost:8000/admin/
4. Customize the organization and user structure as needed
5. Extend with additional features based on requirements
