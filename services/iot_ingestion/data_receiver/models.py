from django.db import models
from django.utils import timezone

class BoilerSite(models.Model):
    """Represents a physical boiler installation site"""
    site_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    installed_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.site_id})"

class Sensor(models.Model):
    """Represents individual sensors on a boiler"""
    SENSOR_TYPES = [
        ('temperature', 'Temperature'),
        ('pressure', 'Pressure'),
        ('fuel_level', 'Fuel Level'),
        ('flow_rate', 'Flow Rate'),
        ('efficiency', 'Efficiency'),
    ]
    
    boiler_site = models.ForeignKey(BoilerSite, on_delete=models.CASCADE, related_name='sensors')
    sensor_id = models.CharField(max_length=50)
    sensor_type = models.CharField(max_length=20, choices=SENSOR_TYPES)
    unit = models.CharField(max_length=20)  # e.g., 'celsius', 'bar', 'liters'
    min_value = models.FloatField(null=True, blank=True)
    max_value = models.FloatField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['boiler_site', 'sensor_id']
    
    def __str__(self):
        return f"{self.boiler_site.name} - {self.sensor_type} ({self.sensor_id})"

class DataIngestionLog(models.Model):
    """Logs data ingestion events for monitoring"""
    timestamp = models.DateTimeField(auto_now_add=True)
    boiler_site = models.ForeignKey(BoilerSite, on_delete=models.CASCADE)
    records_count = models.IntegerField()
    status = models.CharField(max_length=20, choices=[
        ('success', 'Success'),
        ('error', 'Error'),
        ('partial', 'Partial')
    ])
    error_message = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.boiler_site.site_id} - {self.timestamp} - {self.status}"
