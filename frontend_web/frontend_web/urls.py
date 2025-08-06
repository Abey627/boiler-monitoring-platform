"""
Main URL Configuration for Frontend Web Service
User Management Focus - Full Development
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
]
