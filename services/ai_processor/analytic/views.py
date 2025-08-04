from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "ok", "service": "ai_processor"})
