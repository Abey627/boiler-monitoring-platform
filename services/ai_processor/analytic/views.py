from django.http import JsonResponse

# AI Processor Views - Cleaned for Re-implementation

def health_check(request):
    """Health check endpoint for ai_processor service"""
    return JsonResponse({
        "status": "ok", 
        "service": "ai_processor",
        "purpose": "Analytics & ML Processing"
    })
