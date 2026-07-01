# coursemanager/urls.py
# Root URL configuration — delegates to app-level urls

from django.contrib import admin
from django.urls import path, include
from courses.views import hello_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/hello/', hello_view),           # Task 2 - Step 9
    path('api/', include('courses.urls')),    # Delegate all /api/ to courses app
]