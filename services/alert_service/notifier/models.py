from django.db import models
from django.utils import timezone

class AlertRule(models.Model):
    """Defines alert rules for boiler monitoring"""
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    CONDITION_CHOICES = [
        ('above', 'Above Threshold'),
        ('below', 'Below Threshold'),
        ('between', 'Between Values'),
        ('outside', 'Outside Range'),
    ]
    
    site_id = models.CharField(max_length=50)  # Reference to boiler site
    parameter = models.CharField(max_length=100)  # temperature, pressure, etc.
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    threshold_min = models.FloatField(null=True, blank=True)
    threshold_max = models.FloatField(null=True, blank=True)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.site_id} - {self.parameter} - {self.severity}"

class Alert(models.Model):
    """Represents triggered alerts"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('acknowledged', 'Acknowledged'),
        ('resolved', 'Resolved'),
        ('false_positive', 'False Positive'),
    ]
    
    alert_rule = models.ForeignKey(AlertRule, on_delete=models.CASCADE, related_name='alerts')
    triggered_at = models.DateTimeField(default=timezone.now)
    value = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    acknowledged_by = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.alert_rule.site_id} - {self.alert_rule.parameter} - {self.triggered_at}"

class NotificationChannel(models.Model):
    """Defines how alerts are sent (email, SMS, etc.)"""
    CHANNEL_TYPES = [
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('webhook', 'Webhook'),
        ('push', 'Push Notification'),
    ]
    
    name = models.CharField(max_length=255)
    channel_type = models.CharField(max_length=20, choices=CHANNEL_TYPES)
    configuration = models.JSONField()  # Store channel-specific config
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.channel_type})"

class NotificationLog(models.Model):
    """Logs notification attempts"""
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name='notifications')
    channel = models.ForeignKey(NotificationChannel, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('pending', 'Pending')
    ])
    error_message = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.alert} - {self.channel.name} - {self.status}"
