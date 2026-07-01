# ============================================================
# Hands-On 8 – RESTful API Design Best Practices
# main.py (FastAPI implementation)
# Cognizant DN5.0 | Harish Seetharaman Rama
# ============================================================

from typing import Optional, List
from fastapi import FastAPI, HTTPException, status, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(
    title   = "Course Management API v1",
    version = "1.0.0"
)

# ── In-memory store ───────────────────────────────────────
courses_store : List[dict] = [
    {"id": 1, "name": "Data Structures", "code": "CS101", "credits": 4, "department_id": 1},
    {"id": 2, "name": "DBMS",            "code": "CS102", "credits": 3, "department_id": 1},
    {"id": 3, "name": "OOP",             "code": "CS103", "credits": 4, "department_id": 1},
    {"id": 4, "name": "Circuit Theory",  "code": "EC101", "credits": 3, "department_id": 2},
    {"id": 5, "name": "Thermodynamics",  "code": "ME101", "credits": 3, "department_id": 3},
]
_next_id = 6


# ============================================================
# SCHEMAS
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

class PaginatedResponse(BaseModel):
    count   : int
    next    : Optional[str]
    previous: Optional[str]
    results : List[CourseResponse]


# ============================================================
# STANDARD ERROR RESPONSE FORMAT
# ============================================================

def error_response(code: str, message: str, field=None):
    """Standard error format for all endpoints."""
    return {"error": {"code": code, "message": message, "field": field}}


# ============================================================
# TASK 1: Correct REST Naming, HTTP Methods, Status Codes
# ============================================================
# ✅ URLs use NOUNS not verbs (/api/v1/courses/ not /api/v1/getCourses/)
# ✅ URLs are PLURAL
# ✅ HTTP methods are semantically correct
# ✅ Status codes are correct (200, 201, 204, 400, 404)
# ✅ POST returns 201 + Location header
# ✅ DELETE returns 204 No Content

@app.get("/api/v1/courses/",
         response_model=PaginatedResponse,
         tags=["Courses"],
         summary="List courses with pagination and search")
async def list_courses(
    page       : int            = Query(default=1, ge=1),
    page_size  : int            = Query(default=10, ge=1, le=100),
    search     : Optional[str]  = Query(default=None, description="Search by name or code"),
    department_id: Optional[int]= Query(default=None)
):
    """
    TASK 2: Offset pagination with standard envelope response.

    Returns:
    {
        "count": total,
        "next": "/api/v1/courses/?page=2&page_size=2",
        "previous": null,
        "results": [...]
    }

    Versioning strategies (comment):
    1. URL versioning (/api/v1/) — simple and visible, easy to test in browser.
    2. Header versioning (Accept: application/vnd.api+json;version=1)
       — keeps URLs clean but harder to test without tools like Postman.
    URL versioning is preferred for most REST APIs due to its simplicity.
    """
    results = courses_store[:]

    # Search filter (case-insensitive LIKE)
    if search:
        s = search.lower()
        results = [
            c for c in results
            if s in c['name'].lower() or s in c['code'].lower()
        ]

    # Department filter
    if department_id:
        results = [c for c in results if c['department_id'] == department_id]

    total = len(results)
    skip  = (page - 1) * page_size
    page_results = results[skip: skip + page_size]

    # Build next/previous URLs
    base = f"/api/v1/courses/?page_size={page_size}"
    next_url = f"{base}&page={page + 1}" if skip + page_size < total else None
    prev_url = f"{base}&page={page - 1}" if page > 1 else None

    return {
        "count"   : total,
        "next"    : next_url,
        "previous": prev_url,
        "results" : page_results
    }


@app.post("/api/v1/courses/",
          response_model=CourseResponse,
          status_code=status.HTTP_201_CREATED,
          tags=["Courses"])
async def create_course(course: CourseCreate, response: JSONResponse = None):
    global _next_id
    new_course = {"id": _next_id, **course.model_dump()}
    courses_store.append(new_course)
    _next_id += 1

    from fastapi.responses import Response
    from fastapi import Response as FastAPIResponse

    # Return 201 with Location header
    headers = {"Location": f"/api/v1/courses/{new_course['id']}/"}
    return JSONResponse(content=new_course, status_code=201, headers=headers)


@app.get("/api/v1/courses/{course_id}",
         response_model=CourseResponse,
         tags=["Courses"])
async def get_course(course_id: int):
    course = next((c for c in courses_store if c['id'] == course_id), None)
    if not course:
        raise HTTPException(
            status_code=404,
            detail=error_response("NOT_FOUND", f"Course with id {course_id} does not exist")
        )
    return course


@app.put("/api/v1/courses/{course_id}",
         response_model=CourseResponse,
         tags=["Courses"])
async def update_course(course_id: int, course_data: CourseCreate):
    """PUT — full replacement (all fields required)."""
    course = next((c for c in courses_store if c['id'] == course_id), None)
    if not course:
        raise HTTPException(status_code=404,
            detail=error_response("NOT_FOUND", f"Course {course_id} does not exist"))
    course.update(course_data.model_dump())
    return course


@app.patch("/api/v1/courses/{course_id}",
           response_model=CourseResponse,
           tags=["Courses"])
async def partial_update_course(course_id: int, course_data: CourseUpdate):
    """PATCH — partial update (only supplied fields are updated)."""
    course = next((c for c in courses_store if c['id'] == course_id), None)
    if not course:
        raise HTTPException(status_code=404,
            detail=error_response("NOT_FOUND", f"Course {course_id} does not exist"))
    update_data = course_data.model_dump(exclude_unset=True)
    course.update(update_data)
    return course


@app.delete("/api/v1/courses/{course_id}",
            status_code=status.HTTP_204_NO_CONTENT,
            tags=["Courses"])
async def delete_course(course_id: int):
    """DELETE returns 204 No Content — no response body."""
    global courses_store
    course = next((c for c in courses_store if c['id'] == course_id), None)
    if not course:
        raise HTTPException(status_code=404,
            detail=error_response("NOT_FOUND", f"Course {course_id} does not exist"))
    courses_store = [c for c in courses_store if c['id'] != course_id]