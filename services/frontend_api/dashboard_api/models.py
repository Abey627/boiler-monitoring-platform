from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class Organization(models.Model):
    """Represents client organizations using the platform"""
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    contact_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class User(AbstractUser):
    """Extended user model for the platform"""
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('operator', 'Operator'),
        ('viewer', 'Viewer'),
        ('technician', 'Technician'),
    ]
    
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='users')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='viewer')
    phone = models.CharField(max_length=20, blank=True)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    
    # Fix model conflicts with Django's built-in User model
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='dashboard_api_user_set',
        related_query_name='dashboard_api_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='dashboard_api_user_set',
        related_query_name='dashboard_api_user',
    )
    
    def __str__(self):
        return f"{self.username} ({self.organization.name})"

class DashboardConfig(models.Model):
    """Stores dashboard configuration for users/organizations"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dashboard_configs')
    name = models.CharField(max_length=255)
    config = models.JSONField()  # Stores widget layout, preferences, etc.
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.name}"

class SystemStatus(models.Model):
    """Tracks overall system health and status"""
    STATUS_CHOICES = [
        ('healthy', 'Healthy'),
        ('warning', 'Warning'),
        ('critical', 'Critical'),
        ('maintenance', 'Maintenance'),
    ]
    
    service_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    message = models.TextField(blank=True)
    checked_at = models.DateTimeField(auto_now_add=True)
    response_time_ms = models.IntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['-checked_at']
    
    def __str__(self):
        return f"{self.service_name} - {self.status}"

class AuditLog(models.Model):
    """Tracks user actions for compliance and security"""
    ACTION_CHOICES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('view_dashboard', 'View Dashboard'),
        ('acknowledge_alert', 'Acknowledge Alert'),
        ('update_settings', 'Update Settings'),
        ('export_data', 'Export Data'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    resource = models.CharField(max_length=255, blank=True)  # What was accessed
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.JSONField(blank=True, null=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"
