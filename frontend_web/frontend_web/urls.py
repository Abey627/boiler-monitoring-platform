from django.contrib import admin
from django.urls import path
from dashboard.views import (
    health_check, login_view, logout_view, dashboard_view, 
    api_sensor_data, api_historical_data
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check),
    path('', login_view, name='login'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('api/sensor-data/', api_sensor_data, name='api_sensor_data'),
    path('api/historical-data/', api_historical_data, name='api_historical_data'),
]
