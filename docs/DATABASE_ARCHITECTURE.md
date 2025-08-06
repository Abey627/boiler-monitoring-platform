# Database Architecture

## Overview
This project uses a **multi-database architecture** optimized for different data types and access patterns.

## Database Configuration

### PostgreSQL (Primary Database)
- **Purpose**: Business logic, metadata, user management, configurations
- **Host**: `postgres:5432`
- **Database**: `steambytes_core`
- **User**: `steambytes`
- **Used by**: All Django services for business data

**Stores:**
- User accounts and authentication
- Boiler site configurations
- Sensor metadata and settings
- Data ingestion logs
- Alert configurations
- Business logic entities

### InfluxDB (Time-Series Database)
- **Purpose**: High-performance time-series data storage
- **Host**: `influxdb:8086`
- **Organization**: `steambytes`
- **Bucket**: `sensor_data`
- **Used by**: IoT Ingestion (write), AI Processor (read)

**Stores:**
- All sensor readings (temperature, pressure, etc.)
- Historical time-series data
- Data for analytics and trend analysis
- Long-term data retention

### Redis (Cache & Session Store)
- **Purpose**: Real-time caching and session management
- **Host**: `redis:6379`
- **Used by**: All services for different caching needs

**Cache Strategies by Service:**
- **Frontend Web**: Session storage and page caching
- **Frontend API**: API response caching (5 min TTL)
- **IoT Ingestion**: Latest sensor values (5 min TTL), dashboard cache (1 min TTL)
- **AI Processor**: Analytics results caching (30 min TTL)
- **Alert Service**: Alert state and notification caching (5 min TTL)

## Service Database Usage

| Service | PostgreSQL | InfluxDB | Redis | Purpose |
|---------|------------|----------|-------|---------|
| **Frontend Web** | ✅ User auth, sessions | ❌ | ✅ Sessions, caching | Dashboard UI |
| **Frontend API** | ✅ Business data | ❌ | ✅ API caching | Data aggregation |
| **IoT Ingestion** | ✅ Metadata, logs | ✅ Sensor data | ✅ Real-time cache | Data collection |
| **AI Processor** | ✅ Analytics config | ✅ Historical data | ✅ Results cache | Analytics & ML |
| **Alert Service** | ✅ Alert rules | ❌ | ✅ Alert state | Notifications |

## Data Flow

```
IoT Sensors → IoT Ingestion → InfluxDB (Historical)
                     ↓
                  Redis (Real-time) → Frontend API → Dashboard
                     ↓
              AI Processor → PostgreSQL (Results) → Alert Service
```

## Environment Variables

Required environment variables for database connections:

```bash
# PostgreSQL
DB_PASSWORD=steambytes_dev_password
POSTGRES_DB=steambytes_core
POSTGRES_USER=steambytes
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# InfluxDB
INFLUX_URL=http://influxdb:8086
INFLUX_TOKEN=steambytes_admin_token
INFLUX_ORG=steambytes
INFLUX_BUCKET=sensor_data

# Redis
REDIS_URL=redis://redis:6379/0
```

## Development Fallback

For local development without Docker, set:
```bash
USE_SQLITE=true
```

This will make Django services fallback to SQLite for development purposes.

## Performance Benefits

1. **PostgreSQL**: ACID compliance for critical business data
2. **InfluxDB**: 10x faster than traditional databases for time-series queries
3. **Redis**: Sub-millisecond response times for real-time dashboard data

## Cache Key Patterns

- **Latest sensor values**: `latest:{site_id}:{sensor_type}`
- **Dashboard data**: `dashboard:{site_id}`
- **Service prefixes**: `frontend_web:`, `frontend_api:`, `iot_ingestion:`, etc.
