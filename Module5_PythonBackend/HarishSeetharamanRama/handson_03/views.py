from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course, Department, Enrollment, Student
from .serializers import (CourseSerializer, DepartmentSerializer,
                          EnrollmentSerializer, StudentSerializer)


# ── Hello View (from Hands-On 1) ──────────────────────────
def hello_view(request):
    return HttpResponse('Course Management API is running')


# ============================================================
# TASK 1: APIView (manual CRUD)
# ============================================================

class CourseListView(APIView):
    """GET all courses / POST create a course"""

    def get(self, request):
        courses    = Course.objects.select_related('department').all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailView(APIView):
    """GET / PUT / DELETE a single course"""

    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return None

    def get(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(CourseSerializer(course).data)

    def put(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ============================================================
# TASK 2: ViewSets + Router (simpler, same result!)
# ============================================================

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset           = Department.objects.all()
    serializer_class   = DepartmentSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset           = Course.objects.select_related('department').all()
    serializer_class   = CourseSerializer

    # Custom action: GET /api/courses/{id}/students/
    @action(detail=True, methods=['get'], url_path='students')
    def students(self, request, pk=None):
        """Returns all students enrolled in this course."""
        course = self.get_object()
        enrollments = Enrollment.objects.filter(
            course=course
        ).select_related('student')
        students = [e.student for e in enrollments]
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)


class StudentViewSet(viewsets.ModelViewSet):
    queryset         = Student.objects.select_related('department').all()
    serializer_class = StudentSerializer


class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset         = Enrollment.objects.select_related('student', 'course').all()
    serializer_class = EnrollmentSerializer