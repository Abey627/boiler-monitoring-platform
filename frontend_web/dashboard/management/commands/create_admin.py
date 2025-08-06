"""
Simple Django management command to create admin user
This is a fallback command for basic admin user creation
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from dashboard.models import User
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Create admin user if it does not exist'

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                user, created = User.objects.get_or_create(
                    username='admin',
                    defaults={
                        'email': 'admin@steambytes.com',
                        'first_name': 'Admin',
                        'last_name': 'User',
                        'is_superuser': True,
                        'is_staff': True,
                        'role': 'admin'
                    }
                )
                
                if created:
                    user.set_password('admin123')
                    user.save()
                    self.stdout.write(
                        self.style.SUCCESS('Superuser created: admin/admin123')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING('Superuser already exists: admin')
                    )
                    
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating admin user: {str(e)}')
            )
            raise
