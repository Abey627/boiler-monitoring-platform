from django.http import JsonResponse

# Alert Service Views - Cleaned for Re-implementation

def health_check(request):
    """Health check endpoint for alert_service"""
    return JsonResponse({
        "status": "ok", 
        "service": "alert_service",
        "purpose": "Alerting & Notifications"
    })
