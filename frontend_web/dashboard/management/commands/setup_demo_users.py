"""
Django management command to create demo users and organizations
This will set up the complete user management structure with dummy data
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from dashboard.models import Organization, User, UserProfile
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Create demo users and organizations for development and testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete existing demo data and recreate',
        )
        parser.add_argument(
            '--quiet',
            action='store_true',
            help='Minimize output',
        )

    def handle(self, *args, **options):
        if not options['quiet']:
            self.stdout.write(
                self.style.SUCCESS('Setting up demo users and organizations...')
            )
        
        try:
            with transaction.atomic():
                self.setup_demo_data(options)
            
            if not options['quiet']:
                self.stdout.write(
                    self.style.SUCCESS('Demo data setup completed successfully!')
                )
                self.display_user_summary()
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error setting up demo data: {str(e)}')
            )
            raise

    def setup_demo_data(self, options):
        """Set up the complete demo data structure"""
        
        if options.get('reset'):
            self.stdout.write('Resetting existing demo data...')
            self.reset_demo_data()
        
        # 1. Create Platform Superusers
        self.create_platform_superusers()
        
        # 2. Create Platform Operators
        self.create_platform_operators()
        
        # 3. Create Organizations
        acme_corp = self.create_acme_corporation()
        tech_solutions = self.create_tech_solutions()
        
        # 4. Create Organization Users
        self.create_acme_users(acme_corp)
        self.create_tech_solutions_users(tech_solutions)

    def reset_demo_data(self):
        """Reset all demo data (careful - this deletes users!)"""
        # Delete demo organizations (this will cascade to users)
        Organization.objects.filter(
            code__in=['ACME001', 'TECH002']
        ).delete()
        
        # Delete platform users (non-organization users)
        User.objects.filter(
            organization__isnull=True,
            username__in=[
                'ceo', 'head_operations', 'dev_lead',
                'platform_admin', 'platform_operator'
            ]
        ).delete()

    def create_platform_superusers(self):
        """Create system-level superusers"""
        superusers = [
            {
                'username': 'ceo',
                'email': 'ceo@steambytes.com',
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'role': 'admin',
                'is_superuser': True,
                'is_staff': True,
                'department': 'Executive',
                'phone': '+1-555-0001'
            },
            {
                'username': 'head_operations',
                'email': 'head.ops@steambytes.com',
                'first_name': 'Michael',
                'last_name': 'Chen',
                'role': 'admin',
                'is_superuser': True,
                'is_staff': True,
                'department': 'Operations',
                'phone': '+1-555-0002'
            },
            {
                'username': 'dev_lead',
                'email': 'dev.lead@steambytes.com',
                'first_name': 'Emily',
                'last_name': 'Rodriguez',
                'role': 'admin',
                'is_superuser': True,
                'is_staff': True,
                'department': 'Development',
                'phone': '+1-555-0003'
            }
        ]
        
        for user_data in superusers:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults=user_data
            )
            if created:
                user.set_password('admin123')  # Standard demo password
                user.save()
                
                # Create profile
                UserProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'timezone': 'UTC',
                        'language': 'en',
                        'theme': 'light',
                        'email_notifications': True,
                        'alert_frequency': 'immediate'
                    }
                )
                self.stdout.write(f'Created superuser: {user.username}')
            else:
                self.stdout.write(f'Superuser already exists: {user.username}')

    def create_platform_operators(self):
        """Create platform operation team users"""
        operators = [
            {
                'username': 'platform_admin',
                'email': 'admin@steambytes.com',
                'first_name': 'David',
                'last_name': 'Wilson',
                'role': 'admin',
                'is_staff': True,
                'department': 'Platform Operations',
                'phone': '+1-555-0010'
            },
            {
                'username': 'platform_operator',
                'email': 'operator@steambytes.com',
                'first_name': 'Lisa',
                'last_name': 'Anderson',
                'role': 'manager',
                'is_staff': True,
                'department': 'Platform Operations',
                'phone': '+1-555-0011'
            }
        ]
        
        for user_data in operators:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults=user_data
            )
            if created:
                user.set_password('operator123')  # Standard demo password
                user.save()
                
                # Create profile
                UserProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'timezone': 'UTC',
                        'language': 'en',
                        'theme': 'dark',  # Platform ops prefer dark theme
                        'email_notifications': True,
                        'alert_frequency': 'hourly'
                    }
                )
                self.stdout.write(f'Created platform operator: {user.username}')
            else:
                self.stdout.write(f'Platform operator already exists: {user.username}')

    def create_acme_corporation(self):
        """Create ACME Corporation with multiple sites"""
        org, created = Organization.objects.get_or_create(
            code='ACME001',
            defaults={
                'name': 'ACME Corporation',
                'contact_email': 'contact@acmecorp.com',
                'phone': '+1-800-ACME-001',
                'address': '123 Industrial Drive, Manufacturing City, TX 75001',
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write('Created organization: ACME Corporation')
        else:
            self.stdout.write('Organization already exists: ACME Corporation')
            
        return org

    def create_tech_solutions(self):
        """Create Tech Solutions Inc with multiple sites"""
        org, created = Organization.objects.get_or_create(
            code='TECH002',
            defaults={
                'name': 'Tech Solutions Inc',
                'contact_email': 'info@techsolutions.com',
                'phone': '+1-888-TECH-002',
                'address': '456 Innovation Boulevard, Tech Valley, CA 94000',
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write('Created organization: Tech Solutions Inc')
        else:
            self.stdout.write('Organization already exists: Tech Solutions Inc')
            
        return org

    def create_acme_users(self, organization):
        """Create users for ACME Corporation"""
        acme_users = [
            {
                'username': 'acme_admin',
                'email': 'admin@acmecorp.com',
                'first_name': 'John',
                'last_name': 'Smith',
                'role': 'admin',
                'department': 'Operations Management',
                'phone': '+1-800-ACME-101',
                'is_staff': False,
                'profile_settings': {
                    'timezone': 'America/Chicago',
                    'theme': 'light',
                    'alert_frequency': 'immediate'
                }
            },
            {
                'username': 'acme_manager',
                'email': 'manager@acmecorp.com',
                'first_name': 'Jennifer',
                'last_name': 'Davis',
                'role': 'manager',
                'department': 'Site Management',
                'phone': '+1-800-ACME-102',
                'is_staff': False,
                'profile_settings': {
                    'timezone': 'America/Chicago',
                    'theme': 'light',
                    'alert_frequency': 'hourly'
                }
            },
            {
                'username': 'acme_operator1',
                'email': 'operator1@acmecorp.com',
                'first_name': 'Robert',
                'last_name': 'Johnson',
                'role': 'operator',
                'department': 'Plant A Operations',
                'phone': '+1-800-ACME-201',
                'is_staff': False,
                'profile_settings': {
                    'timezone': 'America/Chicago',
                    'theme': 'light',
                    'alert_frequency': 'immediate'
                }
            },
            {
                'username': 'acme_operator2',
                'email': 'operator2@acmecorp.com',
                'first_name': 'Maria',
                'last_name': 'Garcia',
                'role': 'operator',
                'department': 'Plant B Operations',
                'phone': '+1-800-ACME-202',
                'is_staff': False,
                'profile_settings': {
                    'timezone': 'America/Chicago',
                    'theme': 'dark',
                    'alert_frequency': 'immediate'
                }
            },
            {
                'username': 'acme_tech',
                'email': 'tech@acmecorp.com',
                'first_name': 'Kevin',
                'last_name': 'Brown',
                'role': 'technician',
                'department': 'Maintenance',
                'phone': '+1-800-ACME-301',
                'is_staff': False,
                'profile_settings': {
                    'timezone': 'America/Chicago',
                    'theme': 'light',
                    'alert_frequency': 'daily'
                }
            },
            {
                'username': 'acme_viewer',
                'email': 'reporting@acmecorp.com',
                'first_name': 'Amanda',
                'last_name': 'Wilson',
                'role': 'viewer',
                'department': 'Reporting & Analytics',
                'phone': '+1-800-ACME-401',
                'is_staff': False,
                'profile_settings': {
                    'timezone': 'America/Chicago',
                    'theme': 'light',
                    'alert_frequency': 'daily'
                }
            }
        ]
        
        self.create_organization_users(organization, acme_users, 'acme123')

    def create_tech_solutions_users(self, organization):
        """Create users for Tech Solutions Inc"""
        tech_users = [
            {
                'username': 'tech_admin',
                'email': 'admin@techsolutions.com',
                'first_name': 'Alex',
                'last_name': 'Thompson',
                'role': 'admin',
                'department': 'IT Operations',
                'phone': '+1-888-TECH-101',
                'is_staff': False,
                'profile_settings': {
                    'timezone': 'America/Los_Angeles',
                    'theme': 'dark',
                    'alert_frequency': 'immediate'
                }
            },
            {
                'username': 'tech_manager',
                'email': 'manager@techsolutions.com',
                'first_name': 'Rachel',
                'last_name': 'Lee',
                'role': 'manager',
                'department': 'Data Center Management',
                'phone': '+1-888-TECH-102',
                'is_staff': False,
                'profile_settings': {
                    'timezone': 'America/Los_Angeles',
                    'theme': 'dark',
                    'alert_frequency': 'hourly'
                }
            },
            {
                'username': 'tech_operator1',
                'email': 'operator1@techsolutions.com',
                'first_name': 'James',
                'last_name': 'Miller',
                'role': 'operator',
                'department': 'Server Farm Alpha',
                'phone': '+1-888-TECH-201',
                'is_staff': False,
                'profile_settings': {
                    'timezone': 'America/Los_Angeles',
                    'theme': 'dark',
                    'alert_frequency': 'immediate'
                }
            },
            {
                'username': 'tech_operator2',
                'email': 'operator2@techsolutions.com',
                'first_name': 'Sophia',
                'last_name': 'Martinez',
                'role': 'operator',
                'department': 'Server Farm Beta',
                'phone': '+1-888-TECH-202',
                'is_staff': False,
                'profile_settings': {
                    'timezone': 'America/Los_Angeles',
                    'theme': 'light',
                    'alert_frequency': 'immediate'
                }
            },
            {
                'username': 'tech_specialist',
                'email': 'specialist@techsolutions.com',
                'first_name': 'Daniel',
                'last_name': 'Kim',
                'role': 'technician',
                'department': 'Systems Engineering',
                'phone': '+1-888-TECH-301',
                'is_staff': False,
                'profile_settings': {
                    'timezone': 'America/Los_Angeles',
                    'theme': 'dark',
                    'alert_frequency': 'hourly'
                }
            }
        ]
        
        self.create_organization_users(organization, tech_users, 'tech123')

    def create_organization_users(self, organization, users_data, default_password):
        """Create users for a specific organization"""
        for user_data in users_data:
            profile_settings = user_data.pop('profile_settings', {})
            
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    **user_data,
                    'organization': organization
                }
            )
            
            if created:
                user.set_password(default_password)
                user.save()
                
                # Create profile with custom settings
                UserProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'timezone': profile_settings.get('timezone', 'UTC'),
                        'language': 'en',
                        'theme': profile_settings.get('theme', 'light'),
                        'email_notifications': True,
                        'alert_frequency': profile_settings.get('alert_frequency', 'immediate')
                    }
                )
                
                self.stdout.write(f'Created user: {user.username} for {organization.name}')
            else:
                self.stdout.write(f'User already exists: {user.username}')

    def display_user_summary(self):
        """Display summary of created users"""
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('DEMO USER SUMMARY'))
        self.stdout.write('='*60)
        
        # Platform Superusers
        self.stdout.write('\nPLATFORM SUPERUSERS (Developer Team, HOD, CEO):')
        superusers = User.objects.filter(is_superuser=True, organization__isnull=True)
        for user in superusers:
            self.stdout.write(f'  • {user.username} ({user.get_full_name()}) - {user.department}')
            self.stdout.write(f'    Email: {user.email} | Password: admin123')
        
        # Platform Operators
        self.stdout.write('\nPLATFORM OPERATORS (Operation Team):')
        operators = User.objects.filter(
            is_superuser=False, 
            organization__isnull=True,
            is_staff=True
        )
        for user in operators:
            self.stdout.write(f'  • {user.username} ({user.get_full_name()}) - {user.department}')
            self.stdout.write(f'    Email: {user.email} | Password: operator123')
        
        # Organizations
        for org in Organization.objects.all():
            self.stdout.write(f'\n{org.name.upper()} USERS:')
            org_users = User.objects.filter(organization=org).order_by('role', 'username')
            
            for user in org_users:
                role_emoji = {
                    'admin': 'ADMIN', 'manager': 'MANAGER', 'operator': 'OPERATOR', 
                    'technician': 'TECH', 'viewer': 'VIEWER'
                }.get(user.role, 'USER')
                
                password = 'acme123' if org.code == 'ACME001' else 'tech123'
                self.stdout.write(f'  {role_emoji} {user.username} ({user.get_full_name()}) - {user.get_role_display()}')
                self.stdout.write(f'    Email: {user.email} | Password: {password}')
                self.stdout.write(f'    Department: {user.department}')
        
        self.stdout.write('\n' + '='*60)
        self.stdout.write('Access the dashboard at: http://localhost:8000/')
        self.stdout.write('Admin panel at: http://localhost:8000/admin/')
        self.stdout.write('='*60 + '\n')
