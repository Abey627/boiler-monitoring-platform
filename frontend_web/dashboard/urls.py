"""
Dashboard URL Configuration - User Management System
Clean implementation with essential routes only
"""
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Authentication URLs
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    # Dashboard URLs
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    
    # User Management URLs (Functional features)
    path('users/', views.user_list_view, name='user_list'),
    path('users/<int:user_id>/', views.user_detail_view, name='user_detail'),
    
    # API endpoints
    path('api/user-stats/', views.api_user_stats, name='api_user_stats'),
    path('api/toggle-user-status/', views.api_toggle_user_status, name='api_toggle_user_status'),
    
    # Health check for infrastructure
    path('health/', views.health_check, name='health_check'),
]
