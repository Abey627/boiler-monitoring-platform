from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# User Management Models - Clean Implementation
# This will be the foundation for the microservice architecture

class Organization(models.Model):
    """
    Represents client organizations using the boiler monitoring platform
    Each organization can have multiple users and sites
    """
    name = models.CharField(max_length=255, help_text="Organization name")
    code = models.CharField(max_length=50, unique=True, help_text="Unique organization code")
    contact_email = models.EmailField(help_text="Primary contact email")
    phone = models.CharField(max_length=20, blank=True, help_text="Contact phone number")
    address = models.TextField(blank=True, help_text="Organization address")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, help_text="Is organization active")
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.code})"

class User(AbstractUser):
    """
    Extended user model for the boiler monitoring platform
    Includes role-based access control and organization association
    """
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('manager', 'Manager'),
        ('operator', 'Operator'),
        ('technician', 'Technician'),
        ('viewer', 'Viewer'),
    ]
    
    # Organization relationship
    organization = models.ForeignKey(
        Organization, 
        on_delete=models.CASCADE, 
        related_name='users',
        help_text="Organization this user belongs to",
        null=True, 
        blank=True
    )
    
    # Role and permissions
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='viewer',
        help_text="User role determining access level"
    )
    
    # Additional user information
    phone = models.CharField(max_length=20, blank=True, help_text="User phone number")
    department = models.CharField(max_length=100, blank=True, help_text="User department")
    
    # Security and tracking
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Fix Django conflicts with built-in User model
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='dashboard_user_set',
        related_query_name='dashboard_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='dashboard_user_set',
        related_query_name='dashboard_user',
    )
    
    class Meta:
        pass
    
    def __str__(self):
        return f"{self.username} ({self.organization.name}) - {self.get_role_display()}"
    
    def get_full_name(self):
        """Return full name of user"""
        return f"{self.first_name} {self.last_name}".strip()
    
    def has_role(self, role):
        """Check if user has specific role"""
        return self.role == role
    
    def can_manage_users(self):
        """Check if user can manage other users"""
        return self.role in ['admin', 'manager']

class UserProfile(models.Model):
    """
    Additional profile information for users
    Keeps core User model lean while allowing extended customization
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Dashboard preferences
    timezone = models.CharField(max_length=50, default='UTC', help_text="User timezone")
    language = models.CharField(max_length=10, default='en', help_text="Preferred language")
    theme = models.CharField(
        max_length=20, 
        choices=[('light', 'Light'), ('dark', 'Dark')], 
        default='light',
        help_text="UI theme preference"
    )
    
    # Notification preferences  
    email_notifications = models.BooleanField(default=True, help_text="Receive email notifications")
    sms_notifications = models.BooleanField(default=False, help_text="Receive SMS notifications")
    alert_frequency = models.CharField(
        max_length=20,
        choices=[
            ('immediate', 'Immediate'),
            ('hourly', 'Hourly Digest'),
            ('daily', 'Daily Digest'),
        ],
        default='immediate',
        help_text="How often to receive alerts"
    )
    
    # Additional metadata
    # avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)  # Disabled for now - requires Pillow
    avatar = models.CharField(max_length=255, blank=True, null=True, help_text='Avatar URL or placeholder')
    bio = models.TextField(blank=True, help_text="User biography")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} Profile"

class AuditLog(models.Model):
    """
    Audit logging for user actions and system events
    Important for compliance and security monitoring
    """
    ACTION_CHOICES = [
        ('login', 'User Login'),
        ('logout', 'User Logout'),
        ('user_created', 'User Created'),
        ('user_updated', 'User Updated'),
        ('user_deleted', 'User Deleted'),
        ('password_changed', 'Password Changed'),
        ('profile_updated', 'Profile Updated'),
        ('permission_changed', 'Permission Changed'),
    ]
    
    # Who did what
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='audit_logs',
        help_text="User who performed the action"
    )
    action = models.CharField(max_length=50, choices=ACTION_CHOICES, help_text="Action performed")
    target_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='target_audit_logs',
        help_text="User who was affected by the action"
    )
    
    # When and where
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, help_text="Browser/client information")
    
    # Additional details
    details = models.JSONField(blank=True, null=True, help_text="Additional action details")
    success = models.BooleanField(default=True, help_text="Was the action successful")
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp}"
