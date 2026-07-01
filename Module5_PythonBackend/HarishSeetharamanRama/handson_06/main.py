# ============================================================
# Hands-On 6 – FastAPI: Path Parameters, Pydantic & Async
# main.py
# Cognizant DN5.0 | Harish Seetharaman Rama
# pip install fastapi uvicorn sqlalchemy
# Run: uvicorn main:app --reload
# Docs: http://127.0.0.1:8000/docs
# ============================================================

from typing import Optional, List
from fastapi import FastAPI, HTTPException, Depends, status, Query
from pydantic import BaseModel
from datetime import date

# ── FastAPI app instance ──────────────────────────────────
app = FastAPI(
    title       = "Course Management API",
    description = "A REST API for managing courses, students, and enrollments.",
    version     = "1.0.0",
    contact     = {
        "name" : "Harish Seetharaman Rama",
        "email": "harish@college.edu"
    }
)

# ── In-memory DB for demonstration (replaced with real DB in H7) ──
courses_store: List[dict] = []
_next_id = 1


# ============================================================
# PYDANTIC SCHEMAS (Task 1)
# ============================================================

class CourseCreate(BaseModel):
    """Schema for creating a new course — all fields required."""
    name          : str
    code          : str
    credits       : int
    department_id : int


class CourseUpdate(BaseModel):
    """Schema for updating a course — all fields optional (PATCH style)."""
    name          : Optional[str] = None
    code          : Optional[str] = None
    credits       : Optional[int] = None
    department_id : Optional[int] = None


class CourseResponse(BaseModel):
    """Schema for course responses — includes auto-generated id."""
    id            : int
    name          : str
    code          : str
    credits       : int
    department_id : int


class DepartmentResponse(BaseModel):
    """Nested schema — department with its courses."""
    id      : int
    name    : str
    courses : List[CourseResponse] = []


# ============================================================
# ENDPOINTS (Task 1 & 2)
# ============================================================

@app.get("/", tags=["Health"])
async def root():
    return {"message": "Course Management API is running ✅"}


# POST /api/courses/ — FastAPI auto-validates CourseCreate
@app.post(
    "/api/courses/",
    response_model    = CourseResponse,
    status_code       = status.HTTP_201_CREATED,
    tags              = ["Courses"],
    summary           = "Create a new course",
    response_description = "The newly created course"
)
async def create_course(course: CourseCreate):
    """
    Create a course with all required fields.
    FastAPI automatically validates the request body against CourseCreate.
    Returns 422 Unprocessable Entity if validation fails.
    """
    global _next_id
    new_course = {
        "id"           : _next_id,
        "name"         : course.name,
        "code"         : course.code,
        "credits"      : course.credits,
        "department_id": course.department_id
    }
    courses_store.append(new_course)
    _next_id += 1
    return new_course


# GET /api/courses/ — with pagination and filtering (Task 2)
@app.get(
    "/api/courses/",
    response_model = List[CourseResponse],
    tags           = ["Courses"],
    summary        = "List all courses with pagination"
)
async def get_courses(
    skip          : int           = Query(default=0,    ge=0,  description="Skip N records"),
    limit         : int           = Query(default=10,   ge=1,  description="Max records to return"),
    department_id : Optional[int] = Query(default=None,        description="Filter by department")
):
    """
    Returns a paginated list of courses.
    - skip=0&limit=2  → returns first 2
    - skip=2&limit=2  → returns next 2
    """
    results = courses_store
    if department_id is not None:
        results = [c for c in results if c['department_id'] == department_id]
    return results[skip: skip + limit]


# GET /api/courses/{course_id} — path parameter (Task 2)
@app.get(
    "/api/courses/{course_id}",
    response_model = CourseResponse,
    tags           = ["Courses"],
    summary        = "Get a course by ID"
)
async def get_course(course_id: int):
    """
    Path parameter course_id is automatically validated as integer by FastAPI.
    Returns 404 if not found.
    """
    course = next((c for c in courses_store if c['id'] == course_id), None)
    if not course:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail      = f"Course with id {course_id} not found"
        )
    return course


# PUT /api/courses/{course_id} — full update
@app.put(
    "/api/courses/{course_id}",
    response_model = CourseResponse,
    tags           = ["Courses"],
    summary        = "Update a course"
)
async def update_course(course_id: int, course_data: CourseCreate):
    course = next((c for c in courses_store if c['id'] == course_id), None)
    if not course:
        raise HTTPException(status_code=404, detail=f"Course {course_id} not found")
    course.update(course_data.model_dump())
    return course


# DELETE /api/courses/{course_id}
@app.delete(
    "/api/courses/{course_id}",
    status_code = status.HTTP_204_NO_CONTENT,  # No response body
    tags        = ["Courses"],
    summary     = "Delete a course"
)
async def delete_course(course_id: int):
    global courses_store
    course = next((c for c in courses_store if c['id'] == course_id), None)
    if not course:
        raise HTTPException(status_code=404, detail=f"Course {course_id} not found")
    courses_store = [c for c in courses_store if c['id'] != course_id]
    # HTTP 204 = return nothing (correct for DELETE)