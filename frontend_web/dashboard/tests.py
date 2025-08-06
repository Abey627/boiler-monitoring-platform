"""
Test cases for the dashboard application
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Organization, UserProfile, AuditLog

User = get_user_model()


class OrganizationModelTest(TestCase):
    """Test cases for Organization model"""
    
    def setUp(self):
        self.org = Organization.objects.create(
            name="Test Corp",
            code="TEST001",
            contact_email="test@testcorp.com"
        )
    
    def test_organization_creation(self):
        """Test organization is created correctly"""
        self.assertEqual(self.org.name, "Test Corp")
        self.assertEqual(self.org.code, "TEST001")
        self.assertTrue(self.org.is_active)
    
    def test_organization_str(self):
        """Test organization string representation"""
        self.assertEqual(str(self.org), "Test Corp (TEST001)")


class UserModelTest(TestCase):
    """Test cases for User model"""
    
    def setUp(self):
        self.org = Organization.objects.create(
            name="Test Corp",
            code="TEST001",
            contact_email="test@testcorp.com"
        )
        self.user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="testpass123",
            organization=self.org,
            role="operator"
        )
    
    def test_user_creation(self):
        """Test user is created correctly"""
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.organization, self.org)
        self.assertEqual(self.user.role, "operator")
    
    def test_user_permissions(self):
        """Test user permission methods"""
        self.assertFalse(self.user.can_manage_users())
        
        admin_user = User.objects.create_user(
            username="admin",
            role="admin",
            organization=self.org
        )
        self.assertTrue(admin_user.can_manage_users())


class DashboardViewTest(TestCase):
    """Test cases for dashboard views"""
    
    def setUp(self):
        self.client = Client()
        self.org = Organization.objects.create(
            name="Test Corp",
            code="TEST001",
            contact_email="test@testcorp.com"
        )
        self.user = User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="testpass123",
            organization=self.org
        )
    
    def test_login_view(self):
        """Test login view renders correctly"""
        response = self.client.get(reverse('dashboard:login'))
        self.assertEqual(response.status_code, 200)
    
    def test_user_login(self):
        """Test user can login successfully"""
        response = self.client.post(reverse('dashboard:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after login
    
    def test_dashboard_requires_login(self):
        """Test dashboard requires authentication"""
        response = self.client.get(reverse('dashboard:dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_dashboard_authenticated(self):
        """Test dashboard works for authenticated users"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard:dashboard'))
        self.assertEqual(response.status_code, 200)
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get(reverse('dashboard:health_check'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'frontend_web')
