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
Industrial Sensors → IoT Ingestion → Real-time Processing → Dashboard
                                   ↓
                            AI Analytics → Predictive Alerts → Notifications
```

**Microservices Design:**
- **Frontend Web** (`frontend_web/`) - Django web dashboard UI
- **Frontend API** (`services/frontend_api/`) - REST API for dashboard data
- **IoT Ingestion** (`services/iot_ingestion/`) - Real-time sensor data collection
- **AI Processor** (`services/ai_processor/`) - Analytics and predictive algorithms
- **Alert Service** (`services/alert_service/`) - Notification management

**Technology Stack:**
- Frontend: Django web dashboard with real-time updates
- Backend: Python/Django microservices (containerized)
- Databases: PostgreSQL (business data) + Redis (real-time cache)
- Communication: REST APIs between services
- Deployment: Docker Compose orchestration

## 🔧 Service Architecture

| Service | Purpose | Port | Database |
|---------|---------|------|----------|
| **Frontend Web** | Main monitoring dashboard | 8000 | PostgreSQL |
| **Frontend API** | Dashboard data API | 8001 | PostgreSQL |
| **IoT Ingestion** | Sensor data collection | 8002 | PostgreSQL |
| **AI Processor** | Analytics & predictions | 8003 | PostgreSQL |
| **Alert Service** | Notification system | 8004 | PostgreSQL |
| **Redis** | Real-time caching | 6379 | In-memory |

**Key Benefits of Microservice Design:**
- **Scalability** - Each service can be scaled independently
- **Reliability** - Service failures don't affect the entire system
- **Development** - Teams can work on services independently
- **Technology** - Each service can use optimal tech stack

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
- **API Gateway Pattern** - Frontend API aggregates data from other services
- **Event-driven** - Services communicate via REST APIs
- **Shared Database** - All services use PostgreSQL with separate schemas
- **Real-time Cache** - Redis for sub-second dashboard updates

### Development Commands
```bash
# Start all services
docker compose up --build

# Run migrations for specific service
docker compose exec frontend_web python manage.py migrate
docker compose exec iot_ingestion python manage.py migrate

# Create admin user
docker compose exec frontend_web python manage.py createsuperuser

# View service logs
docker compose logs -f frontend_web
docker compose logs -f ai_processor
```

### API Endpoints by Service
- **Frontend API** (`/api/frontend/`) - Dashboard data aggregation
- **IoT Ingestion** (`/api/iot/`) - Sensor data collection
- **AI Processor** (`/api/ai/`) - Analytics and predictions
- **Alert Service** (`/api/alert/`) - Notification management

### Service Dependencies
```
Frontend Web → Frontend API → [IoT Ingestion, AI Processor, Alert Service]
                           ↓
                    PostgreSQL + Redis
```

</details>
