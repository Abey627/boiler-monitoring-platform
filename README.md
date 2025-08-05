# Boiler Monitoring Platform

A mock industrial boiler monitoring platform built with Django microservices architecture.

## 🎯 Purpose

This project demonstrates:
- Microservices architecture using Django
- Real-time data ingestion and monitoring
- Containerized deployment using Docker Compose
- Nginx-based service orchestration

> **Note:** This is a demonstration project with simulated data.

---

## ⚙️ Architecture

```
Client Browser → Nginx (Reverse Proxy) → Frontend Web (Dashboard) → Frontend API → Microservices
                                                                                  ├── IoT Ingestion
                                                                                  ├── AI Processor  
                                                                                  └── Alert Service
                                                                                  
Database Layer:
PostgreSQL (Business Logic) ← → InfluxDB (Time-Series Data) ← → Redis (Cache/Sessions)
```

### Database Architecture
- **PostgreSQL**: Stores business logic, user accounts, site configurations, alert rules, and audit logs
- **InfluxDB**: Optimized for high-frequency IoT sensor data with automatic retention policies
- **Redis**: Provides real-time caching, session management, and message queuing for alerts

### Real-Time Performance Strategy

**Redis doesn't store all IoT data** - that would be inefficient. Instead, it uses a smart caching strategy:

#### **Data Storage Distribution:**
```
┌─────────────────────┬──────────────────┬────────────────────┐
│ Database            │ Data Type        │ Purpose            │
├─────────────────────┼──────────────────┼────────────────────┤
│ InfluxDB            │ ALL sensor data  │ Historical analysis│
│                     │ (months/years)   │ Trend analysis     │
├─────────────────────┼──────────────────┼────────────────────┤
│ Redis               │ Latest values    │ Real-time dashboard│
│                     │ (5-10 minutes)   │ <100ms response    │
├─────────────────────┼──────────────────┼────────────────────┤
│ PostgreSQL          │ Business logic   │ User management    │
│                     │ Configurations   │ Alert rules        │
└─────────────────────┴──────────────────┴────────────────────┘
```

#### **Why This Provides Real-Time Performance:**
- **Dashboard queries**: Redis cache responds in <1ms vs InfluxDB queries taking 100-500ms
- **Latest sensor values**: Instantly available without complex time-series queries
- **Alert processing**: Real-time queuing and processing of notifications
- **Session management**: User preferences and dashboard configs cached for instant loading

### Data Flow
```
IoT Sensors → IoT Ingestion Service → InfluxDB (Raw Data)
                                   ↓
AI Processor ← InfluxDB (Analysis) → PostgreSQL (Results)
     ↓                                       ↓
Alert Service ← PostgreSQL (Rules) → Redis (Queue) → Notifications
     ↓
Frontend API ← PostgreSQL + Redis (Cache) → Dashboard
```

### Nginx Role
Nginx serves as a **reverse proxy** and **load balancer** that:
- Routes incoming requests to appropriate microservices based on URL paths
- Provides a single entry point (port 80) for all services
- Handles SSL termination and static file serving
- Implements API gateway patterns for microservice communication

---

## 🧩 Services

| Service | Description | Port | Database |
|---------|-------------|------|----------|
| `nginx` | Reverse proxy and API gateway | 80 | - |
| `frontend_web` | Dashboard UI with Chart.js & Tailwind CSS | 8000 | PostgreSQL |
| `frontend_api` | REST API serving dashboard data | 8001 | PostgreSQL + Redis |
| `iot_ingestion` | Receives mock IoT data | 8002 | InfluxDB + PostgreSQL |
| `ai_processor` | Data processing and analytics | 8003 | InfluxDB + PostgreSQL |
| `alert_service` | Notification system | 8004 | PostgreSQL + Redis |
| `postgres` | Primary database | 5432 | - |
| `influxdb` | Time-series database for sensor data | 8086 | - |
| `redis` | Cache and session storage | 6379 | - |

---

## 🔧 Tech Stack

- **Language:** Python 3.11
- **Backend:** Django, Django REST Framework
- **Frontend:** Django Templates, Tailwind CSS, Chart.js
- **Databases:** 
  - **PostgreSQL** - Primary database for business logic, users, configurations
  - **InfluxDB** - Time-series database for high-frequency IoT sensor data
  - **Redis** - Cache and session storage for real-time performance
- **Containerization:** Docker, Docker Compose
- **Proxy:** Nginx
- **Analytics:** NumPy, Pandas for data processing

---

## 🚀 Quick Start

```bash
git clone https://github.com/Abey627/boiler-monitoring-platform.git
cd boiler-monitoring-platform

# Build and run all services
docker compose up --build
```

### Database Setup

After the containers are running, set up the databases:

```bash
# Run PostgreSQL migrations for all services
docker compose exec frontend_api python manage.py migrate
docker compose exec iot_ingestion python manage.py migrate  
docker compose exec ai_processor python manage.py migrate
docker compose exec alert_service python manage.py migrate

# Create sample data (optional)
docker compose exec frontend_api python manage.py shell -c "
from dashboard_api.models import Organization
org = Organization.objects.create(name='Demo Industries', code='DEMO', contact_email='demo@steambytes.com')
print(f'Created organization: {org.name}')
"

# Generate sample IoT data
python scripts/generate_sample_data.py
```

**Access Points:**
- Dashboard: http://localhost/ (via nginx proxy)
- InfluxDB UI: http://localhost:8086 (admin/steambytes_influx_password)
- Direct Service Access: http://localhost:8000-8004
- API Endpoints:
  - Frontend API: http://localhost/api/frontend/
  - IoT Ingestion: http://localhost/api/iot/
  - AI Processor: http://localhost/api/ai/
  - Alert Service: http://localhost/api/alert/

## 📂 Project Structure

```
boiler-monitoring-platform/
├── frontend_web/          # Dashboard UI
├── services/              # Microservices
│   ├── frontend_api/      # API service
│   ├── iot_ingestion/     # IoT data ingestion
│   ├── ai_processor/      # Analytics
│   ├── alert_service/     # Notifications
│   └── shared/           # Shared database utilities
├── nginx/                 # Reverse proxy
└── docker-compose.yml     # Container orchestration
```

## 📊 Data Models

### IoT Ingestion Service
- **BoilerSite**: Physical boiler installations
- **Sensor**: Individual sensors (temperature, pressure, fuel level, etc.)
- **DataIngestionLog**: Tracks data ingestion events

### Alert Service  
- **AlertRule**: Configurable alert thresholds and conditions
- **Alert**: Triggered alerts with status tracking
- **NotificationChannel**: Email, SMS, webhook configurations
- **NotificationLog**: Delivery tracking

### Frontend API Service
- **Organization**: Client organizations
- **User**: Extended user model with roles
- **DashboardConfig**: Customizable dashboard layouts
- **AuditLog**: Compliance and security tracking

### AI Processor Service
- **AnalyticsJob**: Background processing jobs
- **PredictiveModel**: Trained ML models for forecasting
- **AnalyticsResult**: Efficiency scores, predictions
- **PerformanceMetric**: Calculated KPIs and trends

---

## 👨‍💻 Author

**Muhammad Syafiq bin Ahmad Nadzri**  
[LinkedIn](https://www.linkedin.com/in/msyafiq-anadzri)

---

*This is a demonstration project with simulated data.*