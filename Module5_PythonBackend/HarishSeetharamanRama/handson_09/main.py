from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

SECRET_KEY = "coursemanager-super-secret-jwt-key-2024"
ALGORITHM  = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI(title="Course Management API — Secured", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context   = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/")
users_store: List[dict] = []
courses_store: List[dict] = []
_user_id = 1
_course_id = 1

class UserRegister(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int; email: str; is_active: bool

class Token(BaseModel):
    access_token: str; token_type: str

class CourseCreate(BaseModel):
    name: str; code: str; credits: int; department_id: int

class CourseResponse(BaseModel):
    id: int; name: str; code: str; credits: int; department_id: int

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def create_access_token(data, expires_delta=None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = next((u for u in users_store if u['email'] == email), None)
    if user is None:
        raise credentials_exception
    return user

@app.post("/api/v1/auth/register/", response_model=UserResponse,
          status_code=status.HTTP_201_CREATED, tags=["Auth"])
async def register(user_data: UserRegister):
    global _user_id
    existing = next((u for u in users_store if u['email'] == user_data.email), None)
    if existing:
        raise HTTPException(status_code=409,
            detail=f"Email {user_data.email} already registered")
    new_user = {"id": _user_id, "email": user_data.email,
                "hashed_password": get_password_hash(user_data.password),
                "is_active": True}
    users_store.append(new_user)
    _user_id += 1
    return {"id": new_user["id"], "email": new_user["email"], "is_active": True}

@app.post("/api/v1/auth/login/", response_model=Token, tags=["Auth"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = next((u for u in users_store if u['email'] == form_data.username), None)
    if not user or not verify_password(form_data.password, user['hashed_password']):
        raise HTTPException(status_code=401, detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"})
    access_token = create_access_token(
        data={"sub": user["email"]},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/v1/courses/", response_model=List[CourseResponse], tags=["Courses"])
async def list_courses():
    return courses_store

@app.post("/api/v1/courses/", response_model=CourseResponse,
          status_code=status.HTTP_201_CREATED, tags=["Courses"])
async def create_course(course: CourseCreate,
                        current_user: dict = Depends(get_current_user)):
    global _course_id
    new_course = {"id": _course_id, **course.model_dump()}
    courses_store.append(new_course)
    _course_id += 1
    return new_course

@app.delete("/api/v1/courses/{course_id}",
            status_code=status.HTTP_204_NO_CONTENT, tags=["Courses"])
async def delete_course(course_id: int,
                        current_user: dict = Depends(get_current_user)):
    global courses_store
    course = next((c for c in courses_store if c['id'] == course_id), None)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    courses_store = [c for c in courses_store if c['id'] != course_id]