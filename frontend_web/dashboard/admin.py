from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import Organization, User, UserProfile, AuditLog

# Organization Admin
@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'contact_email', 'user_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'code', 'contact_email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'contact_email')
        }),
        ('Contact Details', {
            'fields': ('phone', 'address'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_count(self, obj):
        count = obj.users.count()
        if count > 0:
            url = f"/admin/dashboard/user/?organization__id__exact={obj.id}"
            return format_html('<a href="{}">{} users</a>', url, count)
        return '0 users'
    user_count.short_description = 'Users'


# User Profile Inline
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    
    fieldsets = (
        ('Preferences', {
            'fields': ('timezone', 'language', 'theme')
        }),
        ('Notifications', {
            'fields': ('email_notifications', 'sms_notifications', 'alert_frequency')
        }),
        ('Additional Info', {
            'fields': ('avatar', 'bio'),
            'classes': ('collapse',)
        }),
    )


# Custom User Admin
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'get_full_name', 'organization', 'role', 'is_active', 'is_staff', 'last_login']
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'role', 'organization', 'date_joined']
    search_fields = ['username', 'first_name', 'last_name', 'email', 'organization__name']
    ordering = ['organization', 'role', 'username']
    
    # Custom fieldsets for the edit form
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Organization & Role', {'fields': ('organization', 'role', 'department', 'phone')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
        ('Security', {
            'fields': ('last_login_ip',),
            'classes': ('collapse',)
        }),
    )
    
    # Fieldsets for adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name')
        }),
        ('Organization & Role', {
            'fields': ('organization', 'role', 'department', 'phone')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
    )
    
    inlines = [UserProfileInline]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('organization')


# Audit Log Admin
@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'user', 'action', 'target_user', 'success', 'ip_address']
    list_filter = ['action', 'success', 'timestamp']
    search_fields = ['user__username', 'target_user__username', 'action']
    readonly_fields = ['timestamp', 'user', 'action', 'target_user', 'ip_address', 'user_agent', 'details', 'success']
    date_hierarchy = 'timestamp'
    
    def has_add_permission(self, request):
        # Audit logs should not be manually created
        return False
    
    def has_change_permission(self, request, obj=None):
        # Audit logs should not be modified
        return False
