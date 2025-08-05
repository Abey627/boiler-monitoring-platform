# Contributing to Boiler Monitoring Platform

Thank you for your interest in contributing to this project! This guide will help you get started.

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose
- Git
- Python 3.11+ (for local development)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Abey627/boiler-monitoring-platform.git
   cd boiler-monitoring-platform
   ```

2. **Start the development environment**
   ```bash
   docker compose up --build
   ```

3. **Run database migrations** (after containers are up)
   ```bash
   docker compose exec frontend_web python manage.py migrate
   docker compose exec frontend_api python manage.py migrate
   docker compose exec iot_ingestion python manage.py migrate
   docker compose exec ai_processor python manage.py migrate
   docker compose exec alert_service python manage.py migrate
   ```

4. **Access the application**
   - Dashboard: http://localhost/
   - Individual services: http://localhost:8000-8004

## 🛠️ Development Guidelines

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings for functions and classes
- Keep functions small and focused

### Commit Messages
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

### Testing
- Write tests for new features
- Ensure all tests pass before submitting PR
- Run tests with: `docker compose exec <service> python manage.py test`

## 📁 Project Structure

```
boiler-monitoring-platform/
├── frontend_web/          # Dashboard UI (Django)
├── services/              # Microservices
│   ├── frontend_api/      # REST API service
│   ├── iot_ingestion/     # IoT data ingestion
│   ├── ai_processor/      # Data analytics
│   └── alert_service/     # Notification system
├── nginx/                 # Reverse proxy configuration
├── docker-compose.yml     # Container orchestration
├── .env                   # Environment variables
└── README.md              # Project documentation
```

## 🔄 Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Keep changes focused and atomic
   - Test your changes thoroughly

3. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add your descriptive commit message"
   ```

4. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a Pull Request**
   - Provide a clear description of changes
   - Reference any related issues
   - Include screenshots if UI changes are involved

## 🐛 Reporting Issues

When reporting issues, please include:
- Operating system and version
- Docker version
- Steps to reproduce the issue
- Expected vs actual behavior
- Error messages or logs
- Screenshots (if applicable)

## 📋 Pull Request Checklist

- [ ] Code follows project style guidelines
- [ ] Tests have been added/updated
- [ ] All tests pass
- [ ] Documentation has been updated
- [ ] Commit messages are clear and descriptive
- [ ] PR description explains the changes

## 🤝 Getting Help

If you need help:
- Check existing issues and discussions
- Create a new issue with detailed information
- Reach out to the maintainer: [Muhammad Syafiq](https://www.linkedin.com/in/msyafiq-anadzri)

## 📜 License

By contributing, you agree that your contributions will be licensed under the same license as the project.
