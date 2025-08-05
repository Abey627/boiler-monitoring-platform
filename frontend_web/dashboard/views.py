from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json
import random
from datetime import datetime, timedelta

def health_check(request):
    return JsonResponse({"status": "ok", "service": "frontend_web"})

def login_view(request):
    """Login page for the boiler monitoring dashboard"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'dashboard/login.html')

def logout_view(request):
    """Logout the user"""
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    """Main dashboard view showing boiler monitoring data"""
    return render(request, 'dashboard/dashboard.html')

@login_required
def api_sensor_data(request):
    """API endpoint for real-time sensor data (mock data for demo)"""
    # Generate mock sensor data for demonstration
    now = datetime.now()
    mock_data = {
        'timestamp': now.isoformat(),
        'boilers': [
            {
                'id': 1,
                'name': 'Boiler Unit 1',
                'status': 'operational',
                'temperature': round(random.uniform(180, 220), 1),
                'pressure': round(random.uniform(15, 25), 1),
                'flow_rate': round(random.uniform(450, 550), 1),
                'efficiency': round(random.uniform(85, 95), 1),
                'last_maintenance': (now - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
            },
            {
                'id': 2,
                'name': 'Boiler Unit 2', 
                'status': 'operational',
                'temperature': round(random.uniform(175, 215), 1),
                'pressure': round(random.uniform(16, 24), 1),
                'flow_rate': round(random.uniform(420, 580), 1),
                'efficiency': round(random.uniform(82, 93), 1),
                'last_maintenance': (now - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
            },
            {
                'id': 3,
                'name': 'Boiler Unit 3',
                'status': 'warning',
                'temperature': round(random.uniform(190, 235), 1),
                'pressure': round(random.uniform(18, 26), 1),
                'flow_rate': round(random.uniform(380, 480), 1),
                'efficiency': round(random.uniform(75, 88), 1),
                'last_maintenance': (now - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
            }
        ],
        'alerts': [
            {
                'id': 1,
                'boiler_id': 3,
                'severity': 'warning',
                'message': 'Temperature approaching upper threshold',
                'timestamp': (now - timedelta(minutes=15)).isoformat()
            },
            {
                'id': 2,
                'boiler_id': 1,
                'severity': 'info',
                'message': 'Scheduled maintenance due in 3 days',
                'timestamp': (now - timedelta(hours=2)).isoformat()
            }
        ],
        'system_stats': {
            'total_boilers': 3,
            'operational': 2,
            'warning': 1,
            'offline': 0,
            'avg_efficiency': round(random.uniform(83, 92), 1),
            'total_energy_output': round(random.uniform(2500, 3500), 0)
        }
    }
    
    return JsonResponse(mock_data)

@login_required 
def api_historical_data(request):
    """API endpoint for historical sensor data charts"""
    # Generate mock historical data for the last 24 hours
    now = datetime.now()
    historical_data = []
    
    for i in range(24):
        timestamp = now - timedelta(hours=i)
        historical_data.append({
            'timestamp': timestamp.isoformat(),
            'boiler_1_temp': round(random.uniform(180, 220), 1),
            'boiler_2_temp': round(random.uniform(175, 215), 1), 
            'boiler_3_temp': round(random.uniform(190, 235), 1),
            'boiler_1_pressure': round(random.uniform(15, 25), 1),
            'boiler_2_pressure': round(random.uniform(16, 24), 1),
            'boiler_3_pressure': round(random.uniform(18, 26), 1),
        })
    
    # Reverse to get chronological order
    historical_data.reverse()
    
    return JsonResponse({'data': historical_data})
