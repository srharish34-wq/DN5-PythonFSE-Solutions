# courses/views.py
# Handles HTTP requests and returns responses

from django.http import HttpResponse

def hello_view(request):
    """Simple function-based view to verify the app is running."""
    return HttpResponse('Course Management API is running')