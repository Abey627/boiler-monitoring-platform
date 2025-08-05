from django.contrib import admin
from django.urls import path
from data_receiver.views import (
    health_check, 
    ingest_sensor_data, 
    get_site_sensors, 
    get_ingestion_stats,
    get_realtime_data
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health_check'),
    path('api/ingest/', ingest_sensor_data, name='ingest_sensor_data'),
    path('api/sites/<str:site_id>/sensors/', get_site_sensors, name='get_site_sensors'),
    path('api/sites/<str:site_id>/realtime/', get_realtime_data, name='get_realtime_data'),
    path('api/stats/', get_ingestion_stats, name='get_ingestion_stats'),
]
