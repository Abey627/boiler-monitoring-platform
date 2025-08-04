# Boiler Monitoring Platform (Mock Project)

A **mock industrial boiler monitoring platform** built to demonstrate real-world web, IoT, and AI integration using modern backend and frontend architecture.

This project simulates how a real industrial boiler system can be monitored, analyzed, and acted upon using modular Django microservices, async data flows, and rich visual dashboards.

---

## 🎯 Purpose

This project was developed as a **demonstration piece** for showcasing capabilities in:

- Full-stack development (backend + frontend)
- Microservices architecture using Django
- Real-time data ingestion and monitoring
- Integration with AI/ML pipelines
- Containerized deployment using Docker Compose
- Nginx-based service orchestration and routing

> **Note:** This project is not connected to real IoT hardware or sensors. All boiler data is simulated or mocked.

---

## ⚙️ Architecture Overview

```
                +-------------------+
                |    Frontend Web   |   ← Django + Tailwind
                | (Dashboard UI)    |
                +-------------------+
                         |
                         | REST (Chart.js, Async)
                         ↓
                +--------------------+
                |  Frontend API MS   |   ← Serves data to frontend
                +--------------------+
                         ↑
     ┌────────────┬──────────────┬──────────────┐
     ↓            ↓              ↓              ↓
[IOT Data]   [AI/ML Engine]   [Alerts Engine]  [Redis / Cache]
 ingestion     processor         sender
```

All services talk via REST endpoints behind **Nginx reverse proxy**, and share resources like Redis and SQL Server.

---

## 🧩 Microservices Breakdown

| Service Name      | Description                                                        | Django App       |
|-------------------|--------------------------------------------------------------------|------------------|
| `frontend_web`    | Public-facing dashboard with Chart.js & Tailwind CSS               | `dashboard`      |
| `frontend_api`    | Serves dashboard with REST APIs (boiler status, historical data)   | `dashboard_api`  |
| `iot_ingestion`   | Receives mock data from simulated IoT gateway (e.g., Node-RED)     | `data_receiver`  |
| `ai_processor`    | Processes incoming data using AI/ML (e.g., anomaly detection)       | `analytic`       |
| `alert_service`   | Sends alerts (email, SMS) based on thresholds or AI flags          | `notifier`       |

---

## 🔧 Technologies Used

| Category       | Tech Stack                                          |
|----------------|-----------------------------------------------------|
| Language       | Python 3.11                                         |
| Backend        | Django, Django REST Framework                       |
| Frontend       | Django Templates, Tailwind CSS, Chart.js            |
| Database       | Microsoft SQL Server                                |
| Caching        | Redis                                               |
| Containerization | Docker, Docker Compose                           |
| Messaging      | (Future: MQTT or Celery)                            |
| Routing        | Nginx (reverse proxy)                               |
| Orchestration  | Modular microservices under single Git repo         |

---

## ✅ Features Implemented So Far

- [x] Modular Django microservices created
- [x] Health check endpoints wired for all services
- [x] REST-ready project skeleton with `/health` endpoints
- [x] Docker-friendly structure
- [x] Nginx config placeholder
- [ ] Simulated IoT data flow
- [ ] AI/ML logic for data analysis
- [ ] Email/SMS alert triggers
- [ ] Live dashboard with data visualizations

---

## 📂 Project Structure

```bash
boiler-monitoring-platform/
│
├── frontend_web/               # Frontend Django site (Tailwind)
│   └── dashboard/              # Dashboard app
│
├── services/
│   ├── frontend_api/           # API service for frontend
│   ├── iot_ingestion/          # Ingests mock boiler data
│   ├── ai_processor/           # Runs analytics on ingested data
│   └── alert_service/          # Sends alerts (email/SMS)
│
├── nginx/                      # Reverse proxy config
├── docker-compose.yml          # Compose for all services
└── .env                        # Shared environment config
```

---

## 🚀 Getting Started

> ⚠️ Requires: Docker, Docker Compose, Git

```bash
git clone https://github.com/Abey627/boiler-monitoring-platform.git
cd boiler-monitoring-platform

# Build and run all services
docker-compose up --build
```

Then open:

- http://localhost/ → frontend dashboard
- http://localhost/api/frontend/health/ → frontend API
- http://localhost/api/iot/health/ → IoT service
- http://localhost/api/ai/health/ → AI processor
- http://localhost/api/alert/health/ → Alert service

---

## 👨‍💻 Author

**Muhammad Syafiq bin Ahmad Nadzri**  
Web, IoT & AI Developer (SteamBytes Interview Showcase)  
[LinkedIn](https://www.linkedin.com/in/msyafiq-anadzri)

---

## 📌 Disclaimer

This is a **mock/demo project** and not meant for production. Data is simulated. No real IoT device integration is active yet.