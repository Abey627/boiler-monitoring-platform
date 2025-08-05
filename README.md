# 🔥 Industrial Boiler Monitoring Platform

**A modern industrial boiler monitoring system built for real-time operations and predictive maintenance.**

> **🎭 DEMO PROJECT**: This is a portfolio demonstration with simulated data. Not connected to real equipment.

## 🎯 Key Features

- **Real-time monitoring** of boiler units with 30-second updates
- **Predictive alerts** to prevent equipment failures  
- **Performance analytics** for efficiency optimization
- **Mobile-friendly** responsive dashboard
- **Historical data analysis** for trend identification

## 🚀 Quick Setup

```bash
# Clone and start the system
git clone https://github.com/Abey627/boiler-monitoring-platform.git
cd boiler-monitoring-platform
docker compose up --build

# Access dashboard: http://localhost:8000
# Login: admin / steambytes123
```

## 🏗️ Microservice Architecture

**Data Flow:**
```
Industrial Sensors → IoT Ingestion → InfluxDB (Time-series)
                                   ↓
            AI Processor → PostgreSQL ← Frontend API ← Dashboard
                   ↓                        ↑
            Alert Service → Redis Cache ────┘
```

**Microservices Design:**
- **Nginx** - Reverse proxy and load balancer
- **Frontend Web** (`frontend_web/`) - Django web dashboard UI
- **Frontend API** (`services/frontend_api/`) - REST API for dashboard data
- **IoT Ingestion** (`services/iot_ingestion/`) - Real-time sensor data collection
- **AI Processor** (`services/ai_processor/`) - Analytics and predictive algorithms
- **Alert Service** (`services/alert_service/`) - Notification management

**Database Architecture:**
- **PostgreSQL** - Primary database for business logic and application data
- **InfluxDB** - Time-series database optimized for sensor data
- **Redis** - Cache and session store for real-time performance

**Technology Stack:**
- Frontend: Django web dashboard with real-time updates
- Backend: Python/Django microservices (containerized)
- Databases: PostgreSQL + InfluxDB + Redis
- Proxy: Nginx reverse proxy
- Communication: REST APIs between services
- Deployment: Docker Compose orchestration

## 🔧 Service Architecture

| Service | Purpose | Port | Database |
|---------|---------|------|----------|
| **Nginx** | Reverse proxy & load balancer | 80 | - |
| **Frontend Web** | Main monitoring dashboard | 8000 | PostgreSQL |
| **Frontend API** | Dashboard data API | 8001 | PostgreSQL |
| **IoT Ingestion** | Sensor data collection | 8002 | InfluxDB |
| **AI Processor** | Analytics & predictions | 8003 | PostgreSQL |
| **Alert Service** | Notification system | 8004 | PostgreSQL + Redis |
| **PostgreSQL** | Primary business database | 5432 | Persistent storage |
| **InfluxDB** | Time-series sensor database | 8086 | Time-series data |
| **Redis** | Cache & session store | 6379 | In-memory cache |

**Key Benefits of Microservice Design:**
- **Scalability** - Each service can be scaled independently
- **Reliability** - Service failures don't affect the entire system
- **Specialized Databases** - InfluxDB for time-series, PostgreSQL for business logic
- **Load Balancing** - Nginx distributes traffic across services

## 📈 Benefits

- ✅ Centralized monitoring
- ✅ Predictive maintenance
- ✅ Mobile accessibility  
- ✅ Easy Docker deployment
- 📊 Cost savings through optimization
- ⚡ Energy efficiency tracking

## 📞 Contact

**Muhammad Syafiq bin Ahmad Nadzri**  
**LinkedIn**: [linkedin.com/in/msyafiq-anadzri](https://www.linkedin.com/in/msyafiq-anadzri)

<details>
<summary>🔧 Technical Details</summary>

### Microservice Communication
- **Nginx Reverse Proxy** - Routes traffic to appropriate services on port 80
- **Database Specialization** - InfluxDB for sensor time-series, PostgreSQL for business data
- **Caching Layer** - Redis for session management and real-time data caching
- **Service Isolation** - Each service runs in separate Docker containers

### Development Commands
```bash
# Start all services (9 containers total)
docker compose up --build

# Start specific services
docker compose up nginx frontend_web postgres redis

# Run migrations for specific service
docker compose exec frontend_web python manage.py migrate
docker compose exec iot_ingestion python manage.py migrate

# Create admin user
docker compose exec frontend_web python manage.py createsuperuser

# View service logs
docker compose logs -f frontend_web
docker compose logs -f nginx
docker compose logs -f postgres
```

### Database Access
```bash
# PostgreSQL (Business Data)
docker compose exec postgres psql -U steambytes -d steambytes_core

# InfluxDB (Sensor Data)
# Access via http://localhost:8086
# Username: steambytes, Password: steambytes_influx_password

# Redis (Cache)
docker compose exec redis redis-cli
```

### API Endpoints by Service
- **Nginx Proxy** (`http://localhost/`) - Routes to appropriate services
- **Frontend API** (`/api/frontend/`) - Dashboard data aggregation
- **IoT Ingestion** (`/api/iot/`) - Sensor data collection to InfluxDB
- **AI Processor** (`/api/ai/`) - Analytics and predictions
- **Alert Service** (`/api/alert/`) - Notification management

### Service Dependencies
```
Nginx (Port 80) → [All Services]
Frontend Web → Frontend API → PostgreSQL
IoT Ingestion → InfluxDB (Time-series data)
AI Processor → PostgreSQL + InfluxDB
Alert Service → PostgreSQL + Redis
```

</details>
