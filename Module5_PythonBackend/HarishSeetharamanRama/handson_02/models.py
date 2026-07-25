

from django.db import models


class Department(models.Model):
    name         = models.CharField(max_length=100)
    head_of_dept = models.CharField(max_length=100)
    budget       = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Course(models.Model):
    name       = models.CharField(max_length=150)
    code       = models.CharField(max_length=20, unique=True)
    credits    = models.IntegerField()
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, related_name='courses'
    )

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        ordering = ['code']


class Student(models.Model):
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    email           = models.EmailField(unique=True)
    department      = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, related_name='students'
    )
    enrollment_year = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ['last_name', 'first_name']


class Enrollment(models.Model):
    student         = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name='enrollments'
    )
    course          = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='enrollments'
    )
    enrollment_date = models.DateField(auto_now_add=True)
    grade           = models.CharField(max_length=2, null=True, blank=True)

    def __str__(self):
        return f"{self.student} → {self.course}"

    class Meta:
        # Prevent duplicate enrollments — same student, same course
        unique_together = [['student', 'course']]
        ordering = ['enrollment_date']


# ============================================================
# ORM QUERIES (run in python manage.py shell)
# ============================================================
#
# Create departments:
# from courses.models import Department, Course, Student, Enrollment
# from django.db.models import Count, F
#
# d1 = Department.objects.create(name='Computer Science', head_of_dept='Dr. Ramesh', budget=850000)
# d2 = Department.objects.create(name='Electronics', head_of_dept='Dr. Priya', budget=620000)
#
# Create courses:
# c1 = Course.objects.create(name='Data Structures', code='CS101', credits=4, department=d1)
# c2 = Course.objects.create(name='DBMS', code='CS102', credits=3, department=d1)
# c3 = Course.objects.create(name='OOP', code='CS103', credits=4, department=d1)
# c4 = Course.objects.create(name='Circuit Theory', code='EC101', credits=3, department=d2)
#
# Create students:
# s1 = Student.objects.create(first_name='Arjun', last_name='Mehta',
#      email='arjun@college.edu', department=d1, enrollment_year=2022)
# s2 = Student.objects.create(first_name='Priya', last_name='Suresh',
#      email='priya@college.edu', department=d1, enrollment_year=2022)
# s3 = Student.objects.create(first_name='Rohan', last_name='Verma',
#      email='rohan@college.edu', department=d2, enrollment_year=2021)
# s4 = Student.objects.create(first_name='Sneha', last_name='Patel',
#      email='sneha@college.edu', department=d1, enrollment_year=2023)
# s5 = Student.objects.create(first_name='Vikram', last_name='Das',
#      email='vikram@college.edu', department=d1, enrollment_year=2022)
#
# Filter by department (double underscore = JOIN):
# Course.objects.filter(department__name='Computer Science')
#
# Annotate departments with course count:
# Department.objects.annotate(course_count=Count('courses'))
#
# select_related (single SQL query):
# students = Student.objects.select_related('department').all()
#
# F() expression update — 10% raise:
# Department.objects.update(budget=F('budget') * 1.1)