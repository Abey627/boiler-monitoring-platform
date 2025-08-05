# Project Structure

```
boiler-monitoring-platform/
├── frontend_web/          # Frontend Dashboard
│   ├── dashboard/         # Dashboard app
│   ├── frontend_web/      # Django settings
│   └── Dockerfile
│
├── services/              # Microservices
│   ├── frontend_api/      # API service (port 8001)
│   ├── iot_ingestion/     # IoT data ingestion (port 8002)  
│   ├── ai_processor/      # AI/ML processing (port 8003)
│   └── alert_service/     # Notifications (port 8004)
│
├── nginx/                 # Reverse proxy (port 80)
├── docs/                  # Documentation
└── docker-compose.yml     # Container orchestration
```

## Data Flow

```
IoT Data → IoT Ingestion → AI Processor → Alert Service
              ↓              ↓             ↓
          Database → Frontend API → Frontend Web
```
