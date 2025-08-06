# Setup Scripts for Boiler Monitoring Platform

This directory contains initialization and setup scripts for the Boiler Monitoring Platform.

## Scripts Overview

### Setup Scripts (Platform Initialization)
- **`setup.ps1`** - PowerShell setup script (recommended for Windows)
- **`setup_demo_users.ps1`** - Create comprehensive demo users for development
- **`setup_demo_users.sh`** - Create comprehensive demo users (Linux/Mac)

### Initialization Scripts
- **`init/django-init.sh`** - Django service initialization script

### Utility Scripts
- **`generate_sample_data.py`** - Sample data generator for demo purposes
- **`get_ip.ps1`** - Network IP detection for demos/interviews
- **`reset-migrations-oneliner.ps1`** - Quick Django migration reset utility

### Templates
- **`.dockerignore.template`** - Template for service-specific Docker ignore patterns

## Usage

### Quick Start (Windows with PowerShell)
```powershell
.\scripts\setup.ps1
```

### Sample Data Generation
```powershell
# After platform is running
python .\scripts\generate_sample_data.py
```

### Demo User Setup
```powershell
# Windows - Create comprehensive demo users
.\scripts\setup_demo_users.ps1

# Linux/Mac - Create comprehensive demo users  
./scripts/setup_demo_users.sh

# Or manually via Django command
cd frontend_web
python manage.py setup_demo_users
```

### Network IP Detection (for demos)
```powershell
.\scripts\get_ip.ps1
```

### Reset Migrations (if needed)
```powershell
.\scripts\reset-migrations-oneliner.ps1
```

## What the Setup Scripts Do

1. **Environment Check**: Creates a default `.env` file if it doesn't exist
2. **Service Startup**: Builds and starts all Docker containers with proper dependency management
3. **Database Migrations**: Automatically runs Django migrations for all services
4. **Superuser Creation**: Creates a default admin user for development (admin/admin123)
5. **Static Files**: Collects static files for Django services
6. **Health Checks**: Verifies all services are running and responding
7. **Status Report**: Provides service URLs and next steps

## Django Initialization Features

The `django-init.sh` script handles:

- Database connection verification
- Automatic Django migrations
- Development superuser creation
- Static file collection
- Initial data loading (if fixtures exist)
- Service startup

## Health Checks

The health check scripts verify:

- PostgreSQL database connectivity
- Redis cache availability
- InfluxDB API responses
- All Django services (Frontend Web, API, IoT Ingestion, AI Processor, Alert Service)
- Nginx reverse proxy

## Manual Operations

### Run Health Checks Only
The health checks are integrated into the main setup script. To run setup with health checks:
```powershell
.\scripts\setup.ps1
```

To skip health checks during setup:
```powershell
.\scripts\setup.ps1 -SkipHealthCheck
```

### Manual Django Operations
```bash
# Run migrations for a specific service
docker-compose exec frontend_web python manage.py migrate

# Create superuser manually
docker-compose exec frontend_web python manage.py createsuperuser

# Collect static files
docker-compose exec frontend_web python manage.py collectstatic
```

### Reset All Migrations

#### Automated Reset with Docker (Recommended)
```powershell
# PowerShell - Full automated reset
.\scripts\reset-migrations.ps1

# PowerShell - Force reset without prompts, skip backup
.\scripts\reset-migrations.ps1 -Force -SkipBackup
```

#### Manual Reset (Without Docker)
```powershell
# PowerShell - Manual reset (you recreate migrations afterward)
.\scripts\reset-migrations-manual.ps1

# Windows Command Prompt - Manual reset  
scripts\reset-migrations.bat
```

**What the reset scripts do:**
1. **Backup**: Creates timestamped backups of all databases and migration files
2. **Clean**: Removes all migration files (except `__init__.py`)
3. **Reset**: Deletes all SQLite database files
4. **Recreate**: (Automated script only) Creates fresh migrations and applies them

**When to use migration reset:**
- After making major model changes that conflict with existing migrations
- When migrations become corrupted or inconsistent
- When starting fresh development after structural changes
- Before deploying to a new environment

## Environment Variables

The setup script creates a default `.env` file with:

- `DB_PASSWORD` - PostgreSQL password
- `INFLUX_PASSWORD` - InfluxDB password  
- `INFLUX_TOKEN` - InfluxDB admin token
- `DEBUG` - Django debug mode

You can customize these values by editing the `.env` file before running the setup.

## Troubleshooting

### Issue: Static Files Collection Failure
**Problem**: Services failing with `ImproperlyConfigured: You're using the staticfiles app without having set the STATIC_ROOT setting`
**Solution**: ✅ **FIXED** - Added `STATIC_ROOT = BASE_DIR / 'staticfiles'` to all Django settings files

### Issue: Custom User Model Database Constraint
**Problem**: `frontend_api` service failing with `NOT NULL constraint failed: dashboard_api_user.organization_id`
**Solution**: ✅ **FIXED** - Created custom management command `create_admin` that properly creates organization and user

### Issue: Missing Database Migrations
**Problem**: Services reporting "Your models have changes that are not yet reflected in a migration"
**Solution**: ✅ **FIXED** - Migrations automatically created during Docker build

### If Setup Fails
1. Check Docker is running: `docker --version`
2. Check Docker Compose is available: `docker-compose --version`
3. Review logs: `docker-compose logs`
4. Clean up and retry: `docker-compose down && .\scripts\setup.ps1`

### If Health Checks Fail
- Services may need more time to start
- Check individual service logs: `docker-compose logs [service_name]`
- Verify ports are not in use by other applications

### Common Issues
- **Port conflicts**: Ensure ports 80, 5432, 6379, 8000-8004, 8086 are available
- **Memory issues**: Docker may need more memory allocated
- **Permission issues**: Ensure proper permissions on script files

## Default Credentials

For development environment:
- **Admin User**: admin / admin123
- **PostgreSQL**: steambytes / steambytes_dev_password
- **InfluxDB**: steambytes / steambytes_influx_password
