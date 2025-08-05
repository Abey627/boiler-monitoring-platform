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
```

### Nginx Role
Nginx serves as a **reverse proxy** and **load balancer** that:
- Routes incoming requests to appropriate microservices based on URL paths
- Provides a single entry point (port 80) for all services
- Handles SSL termination and static file serving
- Implements API gateway patterns for microservice communication

---

## 🧩 Services

| Service | Description | Port |
|---------|-------------|------|
| `nginx` | Reverse proxy and API gateway | 80 |
| `frontend_web` | Dashboard UI with Chart.js & Tailwind CSS | 8000 |
| `frontend_api` | REST API serving dashboard data | 8001 |
| `iot_ingestion` | Receives mock IoT data | 8002 |
| `ai_processor` | Data processing and analytics | 8003 |
| `alert_service` | Notification system | 8004 |
| `redis` | Cache and session storage | 6379 |

---

## 🔧 Tech Stack

- **Language:** Python 3.11
- **Backend:** Django, Django REST Framework
- **Frontend:** Django Templates, Tailwind CSS, Chart.js
- **Database:** SQLite (dev), Microsoft SQL Server (prod)
- **Cache:** Redis
- **Containerization:** Docker, Docker Compose
- **Proxy:** Nginx

---

## 🚀 Quick Start

```bash
git clone https://github.com/Abey627/boiler-monitoring-platform.git
cd boiler-monitoring-platform

# Build and run all services
docker compose up --build
```

**Access Points:**
- Dashboard: http://localhost/ (via nginx proxy)
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
│   └── alert_service/     # Notifications
├── nginx/                 # Reverse proxy
└── docker-compose.yml     # Container orchestration
```

---

## 👨‍💻 Author

**Muhammad Syafiq bin Ahmad Nadzri**  
[LinkedIn](https://www.linkedin.com/in/msyafiq-anadzri)

---

*This is a demonstration project with simulated data.*