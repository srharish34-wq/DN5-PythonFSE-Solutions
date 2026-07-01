# ============================================================
# Hands-On 3 – URL Routing with DRF Router
# courses/urls.py
# Cognizant DN5.0 | Harish Seetharaman Rama
# ============================================================

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (CourseListView, CourseDetailView,
                    CourseViewSet, DepartmentViewSet,
                    StudentViewSet, EnrollmentViewSet)

# ── Router auto-generates all CRUD URLs ──
router = DefaultRouter()
router.register('courses',     CourseViewSet)
router.register('departments', DepartmentViewSet)
router.register('students',    StudentViewSet)
router.register('enrollments', EnrollmentViewSet)

urlpatterns = [
    # Task 1 - Manual APIView endpoints
    path('manual/courses/',        CourseListView.as_view(),   name='course-list'),
    path('manual/courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),

    # Task 2 - Router-generated ViewSet endpoints
    path('', include(router.urls)),
]

# ============================================================
# AUTO-GENERATED URLs by the router:
# GET    /api/courses/          → list all courses
# POST   /api/courses/          → create a course
# GET    /api/courses/{id}/     → get one course
# PUT    /api/courses/{id}/     → update a course
# PATCH  /api/courses/{id}/     → partial update
# DELETE /api/courses/{id}/     → delete a course
# GET    /api/courses/{id}/students/ → custom action
# ============================================================