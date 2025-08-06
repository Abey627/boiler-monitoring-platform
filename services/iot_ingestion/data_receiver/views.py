from django.http import JsonResponse

# IoT Ingestion Views - Cleaned for Re-implementation

def health_check(request):
    """Health check endpoint for iot_ingestion service"""
    return JsonResponse({
        "status": "ok", 
        "service": "iot_ingestion",
        "purpose": "Sensor Data Ingestion"
    })
