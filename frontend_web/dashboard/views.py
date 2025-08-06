from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
import json

from .models import User, Organization, UserProfile, AuditLog

# User Management Views - Clean Implementation
# Starting fresh for microservice architecture

def health_check(request):
    """Health check endpoint for frontend_web service"""
    return JsonResponse({
        "status": "ok", 
        "service": "frontend_web",
        "purpose": "User Management & Authentication",
        "version": "1.0.0"
    })

# ============================================================================
# AUTHENTICATION VIEWS
# ============================================================================

def login_view(request):
    """User login page and authentication"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    
                    # Log successful login
                    AuditLog.objects.create(
                        user=user,
                        action='login',
                        ip_address=get_client_ip(request),
                        user_agent=request.META.get('HTTP_USER_AGENT', ''),
                        success=True
                    )
                    
                    # Update last login IP
                    user.last_login_ip = get_client_ip(request)
                    user.save(update_fields=['last_login_ip'])
                    
                    messages.success(request, f'Welcome back, {user.get_full_name() or user.username}!')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Your account has been deactivated.')
            else:
                # Log failed login attempt
                AuditLog.objects.create(
                    user=None,
                    action='login',
                    ip_address=get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    success=False,
                    details={'attempted_username': username}
                )
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Please provide both username and password.')
    
    return render(request, 'dashboard/login.html')

def logout_view(request):
    """User logout"""
    if request.user.is_authenticated:
        # Log logout
        AuditLog.objects.create(
            user=request.user,
            action='logout',
            ip_address=get_client_ip(request),
            success=True
        )
        
        username = request.user.username
        logout(request)
        messages.success(request, f'You have been logged out successfully.')
    
    return redirect('dashboard:login')

def register_view(request):
    """User registration - redirect to admin as users are created by administrators"""
    messages.info(request, 'User accounts are created by administrators. Please contact your system administrator.')
    return redirect('dashboard:login')

# ============================================================================
# DASHBOARD VIEWS  
# ============================================================================

@login_required
def dashboard_view(request):
    """Main dashboard for user management"""
    context = {
        'user': request.user,
        'organization': getattr(request.user, 'organization', None),
        'recent_logins': AuditLog.objects.filter(
            action='login',
            success=True
        ).select_related('user')[:5],
        'total_users': User.objects.filter(organization=getattr(request.user, 'organization', None)).count() if hasattr(request.user, 'organization') else 0,
        'active_users': User.objects.filter(
            organization=getattr(request.user, 'organization', None),
            is_active=True
        ).count() if hasattr(request.user, 'organization') else 0,
    }
    return render(request, 'dashboard/dashboard.html', context)

# ============================================================================
# USER MANAGEMENT VIEWS
# ============================================================================

@login_required
@user_passes_test(lambda u: u.can_manage_users())
def user_list_view(request):
    """List all users in the organization"""
    search_query = request.GET.get('search', '')
    role_filter = request.GET.get('role', '')
    
    users = User.objects.filter(organization=request.user.organization).select_related('organization')
    
    # Apply filters
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    if role_filter:
        users = users.filter(role=role_filter)
    
    # Pagination
    paginator = Paginator(users, 25)
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    
    context = {
        'users': users,
        'search_query': search_query,
        'role_filter': role_filter,
        'role_choices': User.ROLE_CHOICES,
    }
    return render(request, 'dashboard/user_list.html', context)

@login_required
@user_passes_test(lambda u: u.can_manage_users())
def user_detail_view(request, user_id):
    """View user details"""
    user = get_object_or_404(User, id=user_id, organization=request.user.organization)
    
    # Get user's recent activity
    recent_activity = AuditLog.objects.filter(user=user).order_by('-timestamp')[:10]
    
    context = {
        'viewed_user': user,
        'recent_activity': recent_activity,
    }
    return render(request, 'dashboard/user_detail.html', context)

@login_required
def profile_view(request):
    """User profile management"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Update user basic info
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.phone = request.POST.get('phone', '')
        request.user.department = request.POST.get('department', '')
        request.user.save()
        
        # Update profile preferences
        profile.timezone = request.POST.get('timezone', 'UTC')
        profile.language = request.POST.get('language', 'en')
        profile.theme = request.POST.get('theme', 'light')
        profile.email_notifications = request.POST.get('email_notifications') == 'on'
        profile.sms_notifications = request.POST.get('sms_notifications') == 'on'
        profile.alert_frequency = request.POST.get('alert_frequency', 'immediate')
        profile.bio = request.POST.get('bio', '')
        profile.save()
        
        # Log profile update
        AuditLog.objects.create(
            user=request.user,
            action='profile_updated',
            ip_address=get_client_ip(request),
            success=True
        )
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')
    
    context = {
        'profile': profile,
    }
    return render(request, 'dashboard/profile.html', context)

# ============================================================================
# API ENDPOINTS
# ============================================================================

@login_required
def api_user_stats(request):
    """API endpoint for user statistics"""
    org = request.user.organization
    
    stats = {
        'total_users': User.objects.filter(organization=org).count(),
        'active_users': User.objects.filter(organization=org, is_active=True).count(),
        'users_by_role': {},
        'recent_signups': User.objects.filter(
            organization=org,
            date_joined__gte=timezone.now() - timezone.timedelta(days=30)
        ).count(),
        'recent_logins': AuditLog.objects.filter(
            user__organization=org,
            action='login',
            success=True,
            timestamp__gte=timezone.now() - timezone.timedelta(days=7)
        ).count()
    }
    
    # Count users by role
    for role_code, role_name in User.ROLE_CHOICES:
        stats['users_by_role'][role_code] = User.objects.filter(
            organization=org,
            role=role_code
        ).count()
    
    return JsonResponse(stats)

@csrf_exempt
@require_http_methods(["POST"])
@login_required
@user_passes_test(lambda u: u.can_manage_users())
def api_toggle_user_status(request):
    """API endpoint to activate/deactivate users"""
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        
        user = get_object_or_404(User, id=user_id, organization=request.user.organization)
        
        # Don't allow deactivating yourself
        if user == request.user:
            return JsonResponse({'error': 'Cannot deactivate your own account'}, status=400)
        
        # Toggle status
        user.is_active = not user.is_active
        user.save()
        
        # Log the action
        AuditLog.objects.create(
            user=request.user,
            action='user_updated',
            target_user=user,
            ip_address=get_client_ip(request),
            details={
                'action': 'status_toggled',
                'new_status': 'active' if user.is_active else 'inactive'
            },
            success=True
        )
        
        return JsonResponse({
            'success': True,
            'message': f'User {user.username} has been {"activated" if user.is_active else "deactivated"}',
            'new_status': user.is_active
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def is_admin_or_manager(user):
    """Check if user is admin or manager"""
    return user.is_authenticated and user.role in ['admin', 'manager']
