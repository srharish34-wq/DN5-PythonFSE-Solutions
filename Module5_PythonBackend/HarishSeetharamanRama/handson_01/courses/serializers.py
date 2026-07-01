# ============================================================
# Hands-On 3 – Django REST Views, URL Routing & DRF
# courses/serializers.py
# Cognizant DN5.0 | Harish Seetharaman Rama
# ============================================================

from rest_framework import serializers
from .models import Department, Course, Student, Enrollment


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Department
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(
        source='department.name', read_only=True
    )

    class Meta:
        model  = Course
        fields = ['id', 'name', 'code', 'credits', 'department', 'department_name']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Student
        fields = '__all__'


class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(
        source='student.__str__', read_only=True
    )
    course_name = serializers.CharField(
        source='course.name', read_only=True
    )

    class Meta:
        model  = Enrollment
        fields = ['id', 'student', 'student_name', 'course',
                  'course_name', 'enrollment_date', 'grade']