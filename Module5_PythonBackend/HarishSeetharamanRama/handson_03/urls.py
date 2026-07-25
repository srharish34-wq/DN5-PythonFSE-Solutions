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

