from django.urls import path
from dashboard_api.views import health_check

# Minimal URL configuration - Health check only
urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('api/health/', health_check, name='api_health_check'),
    path('', health_check, name='root'),  # Default route
]
