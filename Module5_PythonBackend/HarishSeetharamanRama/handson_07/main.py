# ============================================================
# Hands-On 7 – FastAPI: Dependency Injection, CRUD & Background Tasks
# main.py
# Cognizant DN5.0 | Harish Seetharaman Rama
# pip install fastapi uvicorn sqlalchemy
# Run: uvicorn main:app --reload
# ============================================================

from typing import Optional, List
from fastapi import FastAPI, HTTPException, Depends, status, BackgroundTasks
from pydantic import BaseModel
from datetime import date
import time

app = FastAPI(
    title       = "Course Management API",
    description = "Full CRUD with Background Tasks, Dependency Injection & OpenAPI docs.",
    version     = "2.0.0",
    contact     = {"name": "Harish Seetharaman Rama", "email": "harish@college.edu"}
)

# ── In-memory stores ──────────────────────────────────────
courses_store     : List[dict] = []
students_store    : List[dict] = []
enrollments_store : List[dict] = []
_course_id = 1
_student_id = 1
_enrollment_id = 1


# ============================================================
# PYDANTIC SCHEMAS
# ============================================================

class CourseCreate(BaseModel):
    name: str; code: str; credits: int; department_id: int

class CourseUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    credits: Optional[int] = None
    department_id: Optional[int] = None

class CourseResponse(BaseModel):
    id: int; name: str; code: str; credits: int; department_id: int

class StudentCreate(BaseModel):
    first_name: str; last_name: str; email: str
    department_id: int; enrollment_year: int

class StudentResponse(BaseModel):
    id: int; first_name: str; last_name: str
    email: str; department_id: int; enrollment_year: int

class EnrollmentCreate(BaseModel):
    student_id: int; course_id: int
    enrollment_date: date

class EnrollmentResponse(BaseModel):
    id: int; student_id: int; course_id: int
    enrollment_date: date; grade: Optional[str] = None


# ============================================================
# BACKGROUND TASK
# ============================================================

def send_confirmation_email(student_email: str, course_name: str):
    """
    Simulates sending an email confirmation.
    Runs AFTER the response is sent — client doesn't wait for this.
    Background tasks are useful for non-critical work (emails, logging).
    """
    time.sleep(1)  # simulate email sending delay
    print(f"📧 Sending confirmation to {student_email} for course: {course_name}")


# ============================================================
# COURSE ENDPOINTS (Task 1)
# ============================================================

@app.get("/", tags=["Health"])
async def root():
    return {"message": "Course Management API v2.0 ✅"}


@app.post("/api/courses/",
          response_model=CourseResponse,
          status_code=status.HTTP_201_CREATED,
          tags=["Courses"],
          summary="Create a new course",
          response_description="The newly created course")
async def create_course(course: CourseCreate):
    global _course_id
    new_course = {"id": _course_id, **course.model_dump()}
    courses_store.append(new_course)
    _course_id += 1
    return new_course


@app.get("/api/courses/", response_model=List[CourseResponse], tags=["Courses"])
async def list_courses(skip: int = 0, limit: int = 10):
    return courses_store[skip: skip + limit]


@app.get("/api/courses/{course_id}", response_model=CourseResponse, tags=["Courses"])
async def get_course(course_id: int):
    course = next((c for c in courses_store if c['id'] == course_id), None)
    if not course:
        raise HTTPException(status_code=404, detail=f"Course with id {course_id} not found")
    return course


@app.put("/api/courses/{course_id}", response_model=CourseResponse, tags=["Courses"])
async def update_course(course_id: int, course_data: CourseCreate):
    course = next((c for c in courses_store if c['id'] == course_id), None)
    if not course:
        raise HTTPException(status_code=404, detail=f"Course {course_id} not found")
    course.update(course_data.model_dump())
    return course


@app.patch("/api/courses/{course_id}", response_model=CourseResponse, tags=["Courses"])
async def partial_update_course(course_id: int, course_data: CourseUpdate):
    """PATCH — update only the supplied fields (unlike PUT which needs all fields)."""
    course = next((c for c in courses_store if c['id'] == course_id), None)
    if not course:
        raise HTTPException(status_code=404, detail=f"Course {course_id} not found")
    update_data = course_data.model_dump(exclude_unset=True)
    course.update(update_data)
    return course


@app.delete("/api/courses/{course_id}",
            status_code=status.HTTP_204_NO_CONTENT,
            tags=["Courses"])
async def delete_course(course_id: int):
    global courses_store
    course = next((c for c in courses_store if c['id'] == course_id), None)
    if not course:
        raise HTTPException(status_code=404, detail=f"Course {course_id} not found")
    courses_store = [c for c in courses_store if c['id'] != course_id]


@app.get("/api/courses/{course_id}/students/",
         response_model=List[StudentResponse],
         tags=["Courses"])
async def get_course_students(course_id: int):
    """Returns all students enrolled in this course."""
    enrolled_student_ids = [
        e['student_id'] for e in enrollments_store if e['course_id'] == course_id
    ]
    students = [s for s in students_store if s['id'] in enrolled_student_ids]
    return students


# ============================================================
# STUDENT ENDPOINTS
# ============================================================

@app.post("/api/students/",
          response_model=StudentResponse,
          status_code=status.HTTP_201_CREATED,
          tags=["Students"])
async def create_student(student: StudentCreate):
    global _student_id
    new_student = {"id": _student_id, **student.model_dump()}
    students_store.append(new_student)
    _student_id += 1
    return new_student


@app.get("/api/students/", response_model=List[StudentResponse], tags=["Students"])
async def list_students():
    return students_store


# ============================================================
# ENROLLMENT ENDPOINTS (with Background Task)
# ============================================================

@app.post("/api/enrollments/",
          response_model=EnrollmentResponse,
          status_code=status.HTTP_201_CREATED,
          tags=["Enrollments"],
          summary="Enroll a student in a course")
async def create_enrollment(
    enrollment    : EnrollmentCreate,
    background_tasks: BackgroundTasks   # FastAPI injects this automatically
):
    """
    Enrolls a student in a course.
    After saving, sends a confirmation email in the background.
    The endpoint returns 201 IMMEDIATELY — client doesn't wait for the email.
    """
    global _enrollment_id

    # Check student exists
    student = next((s for s in students_store if s['id'] == enrollment.student_id), None)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Check course exists
    course = next((c for c in courses_store if c['id'] == enrollment.course_id), None)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    new_enrollment = {
        "id"             : _enrollment_id,
        "student_id"     : enrollment.student_id,
        "course_id"      : enrollment.course_id,
        "enrollment_date": enrollment.enrollment_date,
        "grade"          : None
    }
    enrollments_store.append(new_enrollment)
    _enrollment_id += 1

    # Add background task — runs AFTER response is sent
    background_tasks.add_task(
        send_confirmation_email,
        student_email = student['email'],
        course_name   = course['name']
    )

    return new_enrollment