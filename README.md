# 🔥 Industrial Boiler Monitoring Platform

**A modern industrial boiler monitoring system built for real-time operations and predictive maintenance.**

> **🎭 MOCK PROJECT**: This is a demonstration project with simulated data for portfolio purposes.

> **Live Demo**: Login at http://localhost:8000 with `admin` / `steambytes123`

---

## 🎯 What This System Does

- **Real-time monitoring** of all boiler units from a single dashboard
- **Predictive alerts** to prevent costly equipment failures  
- **Performance analytics** to optimize efficiency and reduce energy costs
- **Compliance reporting** for safety and regulatory requirements
- **Mobile-friendly** interface that works on phones, tablets, and computers
- **Live temperature, pressure, and flow monitoring** with 30-second updates
- **Smart alerting system** for maintenance scheduling and emergency response
- **Historical data analysis** to identify trends and optimization opportunities

---

## 🚀 Quick Demo Setup

```bash
# 1. Download the project
git clone https://github.com/Abey627/boiler-monitoring-platform.git
cd boiler-monitoring-platform

# 2. Start the system (takes 2-3 minutes first time)
docker compose up --build

# 3. Open your browser to: http://localhost:8000
# Login: admin / steambytes123
```

**That's it!** The system starts with sample data ready for demonstration.

---

## 📊 Dashboard Features

| Feature | Business Value |
|---------|----------------|
| **Live Monitoring** | See all boiler status at a glance |
| **Alert Management** | Prevent equipment failures before they happen |
| **Performance Metrics** | Track efficiency and optimize energy usage |
| **Historical Charts** | Identify trends and plan maintenance schedules |
| **Mobile Access** | Monitor operations from anywhere |
| **User Management** | Control access and maintain security |

---

## 🏗️ System Architecture (Technical Overview)

### Simple View
```
📱 User Dashboard → 🌐 Web Server → 🔧 Monitoring Services → 📊 Databases
```

### Detailed Architecture
```
Industrial Sensors → Data Collection → Real-time Processing → User Dashboard
                                    ↓
                            Alert System → Notifications
                                    ↓
                              Data Storage → Analytics & Reporting
```

### Technology Stack
- **Frontend**: Modern web dashboard with real-time charts
- **Backend**: Python/Django microservices architecture  
- **Databases**: PostgreSQL (business data) + InfluxDB (sensor data) + Redis (real-time cache)
- **Deployment**: Docker containers for easy installation and scaling

---

## 🔧 System Components

| Component | Purpose | Access |
|-----------|---------|--------|
| **Dashboard** | Main monitoring interface | http://localhost:8000 |
| **API Services** | Data processing and business logic | Background services |
| **Database** | Data storage and analytics | Background services |
| **Alert System** | Notifications and warnings | Integrated in dashboard |

---

## 📈 Key Benefits

- ✅ **Centralized monitoring** - All boiler data in one place
- ✅ **Reduced downtime** - Early warning system prevents failures
- ✅ **Mobile access** - Monitor from anywhere, anytime
- ✅ **Easy deployment** - Set up in minutes, not days
- 📊 **Cost savings** through predictive maintenance
- ⚡ **Energy optimization** with performance analytics
- 📱 **Improved safety** with real-time alerts
- 📋 **Compliance** with automated reporting

---

## 🎥 Demo Scenarios

### Scenario 1: Daily Operations
1. Login to dashboard
2. Check system overview (3 boilers operational)
3. Review temperature trends chart
4. Check active alerts and maintenance schedule

### Scenario 2: Mobile Monitoring
1. Open dashboard on mobile device
2. View condensed metrics optimized for small screens
3. Receive push notifications for critical alerts
4. Quick status check while on-site

### Scenario 3: Maintenance Planning
1. Review historical performance data
2. Identify efficiency trends and patterns
3. Schedule preventive maintenance based on analytics
4. Track maintenance history and compliance

---

## 📞 Support & Contact

**Contact**: Muhammad Syafiq bin Ahmad Nadzri  
**LinkedIn**: [linkedin.com/in/msyafiq-anadzri](https://www.linkedin.com/in/msyafiq-anadzri)

**Project Features:**
- APIs available for connecting existing systems
- Dashboard and alerts can be tailored to specific needs
- Architecture supports multiple facilities and thousands of sensors
- Complete containerized deployment for easy setup

---

<details>
<summary>🔧 Technical Details (Click to expand)</summary>

## Detailed Technical Architecture

### Microservices Design
- **Frontend Web**: Dashboard UI with responsive design
- **Frontend API**: REST API for dashboard data
- **IoT Ingestion**: Real-time sensor data collection
- **AI Processor**: Analytics and predictive algorithms
- **Alert Service**: Notification management

### Database Strategy
- **PostgreSQL**: Business logic, users, configurations
- **InfluxDB**: Time-series sensor data (optimized for IoT)
- **Redis**: Real-time caching for <100ms dashboard response

### Performance Features
- **Real-time updates**: 30-second refresh cycles
- **Responsive design**: Works on all device sizes
- **Scalable architecture**: Supports multiple facilities
- **High availability**: Containerized deployment

### Development Commands
```bash
# Setup development environment
docker compose up --build

# Run database migrations
docker compose exec frontend_web python manage.py migrate

# Create admin user
docker compose exec frontend_web python manage.py createsuperuser

# View logs
docker compose logs -f frontend_web
```

### API Endpoints
- **Dashboard API**: `/api/frontend/`
- **Sensor Data**: `/api/iot/`
- **Analytics**: `/api/ai/`
- **Alerts**: `/api/alert/`

</details>

---

> **📝 Note**: This is a demonstration project created for portfolio purposes. All data shown is simulated and not connected to real industrial equipment.
```
Industrial Sensors → Data Collection → Real-time Processing → User Dashboard
                                    ↓
                            Alert System → Notifications
                                    ↓
                              Data Storage → Analytics & Reporting
```

### Technology Stack
- **Frontend**: Modern web dashboard with real-time charts
- **Backend**: Python/Django microservices architecture  
- **Databases**: PostgreSQL (business data) + InfluxDB (sensor data) + Redis (real-time cache)
- **Deployment**: Docker containers for easy installation and scaling

---

## 🔧 System Components

| Component | Purpose | Access |
|-----------|---------|--------|
| **Dashboard** | Main monitoring interface | http://localhost:8000 |
| **API Services** | Data processing and business logic | Background services |
| **Database** | Data storage and analytics | Background services |
| **Alert System** | Notifications and warnings | Integrated in dashboard |

---

## � Business Benefits

### Immediate Benefits
- ✅ **Centralized monitoring** - All boiler data in one place
- ✅ **Reduced downtime** - Early warning system prevents failures
- ✅ **Mobile access** - Monitor from anywhere, anytime
- ✅ **Easy deployment** - Set up in minutes, not days

### Long-term Benefits  
- 📊 **Cost savings** through predictive maintenance
- ⚡ **Energy optimization** with performance analytics
- 📱 **Improved safety** with real-time alerts
- 📋 **Compliance** with automated reporting

---

## 🎥 Demo Scenarios

### Scenario 1: Daily Operations
1. Login to dashboard
2. Check system overview (3 boilers operational)
3. Review temperature trends chart
4. Check active alerts and maintenance schedule

### Scenario 2: Mobile Monitoring
1. Open dashboard on mobile device
2. View condensed metrics optimized for small screens
3. Receive push notifications for critical alerts
4. Quick status check while on-site

### Scenario 3: Maintenance Planning
1. Review historical performance data
2. Identify efficiency trends and patterns
3. Schedule preventive maintenance based on analytics
4. Track maintenance history and compliance

---

## 📞 Support & Contact

**Contact**: Muhammad Syafiq bin Ahmad Nadzri  
**LinkedIn**: [linkedin.com/in/msyafiq-anadzri](https://www.linkedin.com/in/msyafiq-anadzri)

**Project Features:**
- APIs available for connecting existing systems
- Dashboard and alerts can be tailored to specific needs
- Architecture supports multiple facilities and thousands of sensors
- Complete containerized deployment for easy setup

---

> **📝 Note**: This is a demonstration project created for portfolio purposes. All data shown is simulated and not connected to real industrial equipment.