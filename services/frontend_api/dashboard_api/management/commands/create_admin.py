from django.core.management.base import BaseCommand
from django.db import transaction
from dashboard_api.models import Organization, User


class Command(BaseCommand):
    help = 'Creates a default admin user with organization for development'

    def handle(self, *args, **options):
        try:
            with transaction.atomic():
                # Create default organization if it doesn't exist
                org, created = Organization.objects.get_or_create(
                    code='steambytes',
                    defaults={
                        'name': 'SteamBytes Corporation',
                        'contact_email': 'admin@steambytes.com',
                        'is_active': True
                    }
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'Created organization: {org.name}')
                    )

                # Create admin user if it doesn't exist
                if not User.objects.filter(username='admin').exists():
                    user = User.objects.create_superuser(
                        username='admin',
                        email='admin@steambytes.com',
                        password='admin123',
                        organization=org,
                        role='admin'
                    )
                    self.stdout.write(
                        self.style.SUCCESS('Superuser created: admin/admin123')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING('Superuser already exists')
                    )

        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating superuser: {str(e)}')
            )
