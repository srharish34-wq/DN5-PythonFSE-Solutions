# ============================================================
# Module 3 – Hands On 6: SQLAlchemy ORM — models.py
# Cognizant DN5.0 | Harish Seetharaman Rama
# pip install sqlalchemy psycopg2-binary mysql-connector-python
# ============================================================

from sqlalchemy import (
    create_engine, Column, Integer, String,
    Date, Numeric, ForeignKey, Boolean, Time, CheckConstraint
)
from sqlalchemy.orm import declarative_base, relationship, Session

# ── Change to your DB credentials ──
# PostgreSQL: "postgresql+psycopg2://user:password@localhost/college_db_orm"
# MySQL:      "mysql+mysqlconnector://root:cognizant123@127.0.0.1/college_db_orm"
DATABASE_URL = "mysql+mysqlconnector://root:cognizant123@127.0.0.1/college_db_orm"

engine = create_engine(DATABASE_URL, echo=True)  # echo=True prints all SQL
Base   = declarative_base()

# ============================================================
# Model 1: Department
# ============================================================
class Department(Base):
    __tablename__ = "departments"

    department_id = Column(Integer, primary_key=True, autoincrement=True)
    dept_name     = Column(String(100), nullable=False)
    hod_name      = Column(String(100))
    budget        = Column(Numeric(12, 2))

    students   = relationship("Student",        back_populates="department")
    courses    = relationship("Course",         back_populates="department")
    professors = relationship("Professor",      back_populates="department")

    def __repr__(self):
        return f"<Department(id={self.department_id}, name={self.dept_name})>"


# ============================================================
# Model 2: Student
# ============================================================
class Student(Base):
    __tablename__ = "students"

    student_id      = Column(Integer, primary_key=True, autoincrement=True)
    first_name      = Column(String(50),  nullable=False)
    last_name       = Column(String(50),  nullable=False)
    email           = Column(String(100), unique=True, nullable=False)
    date_of_birth   = Column(Date)
    department_id   = Column(Integer, ForeignKey("departments.department_id"))
    enrollment_year = Column(Integer)
    is_active       = Column(Boolean, default=True)   # added in migration 2

    department  = relationship("Department", back_populates="students")
    enrollments = relationship("Enrollment", back_populates="student")

    def __repr__(self):
        return f"<Student(id={self.student_id}, name={self.first_name} {self.last_name})>"


# ============================================================
# Model 3: Course
# ============================================================
class Course(Base):
    __tablename__ = "courses"

    course_id     = Column(Integer, primary_key=True, autoincrement=True)
    course_name   = Column(String(150), nullable=False)
    course_code   = Column(String(20),  unique=True)
    credits       = Column(Integer)
    department_id = Column(Integer, ForeignKey("departments.department_id"))

    department  = relationship("Department", back_populates="courses")
    enrollments = relationship("Enrollment", back_populates="course")
    schedules   = relationship("CourseSchedule", back_populates="course")

    def __repr__(self):
        return f"<Course(code={self.course_code}, name={self.course_name})>"


# ============================================================
# Model 4: Enrollment
# ============================================================
class Enrollment(Base):
    __tablename__ = "enrollments"

    enrollment_id   = Column(Integer, primary_key=True, autoincrement=True)
    student_id      = Column(Integer, ForeignKey("students.student_id"))
    course_id       = Column(Integer, ForeignKey("courses.course_id"))
    enrollment_date = Column(Date)
    grade           = Column(String(2),
                             CheckConstraint("grade IN ('A','B','C','D','F')"))

    student = relationship("Student", back_populates="enrollments")
    course  = relationship("Course",  back_populates="enrollments")

    def __repr__(self):
        return f"<Enrollment(student={self.student_id}, course={self.course_id}, grade={self.grade})>"


# ============================================================
# Model 5: Professor
# ============================================================
class Professor(Base):
    __tablename__ = "professors"

    professor_id  = Column(Integer, primary_key=True, autoincrement=True)
    prof_name     = Column(String(100), nullable=False)
    email         = Column(String(100), unique=True)
    department_id = Column(Integer, ForeignKey("departments.department_id"))
    salary        = Column(Numeric(10, 2))

    department = relationship("Department", back_populates="professors")

    def __repr__(self):
        return f"<Professor(name={self.prof_name}, salary={self.salary})>"


# ============================================================
# Model 6: CourseSchedule (added in Hands-On 7 migration)
# ============================================================
class CourseSchedule(Base):
    __tablename__ = "course_schedules"

    schedule_id  = Column(Integer, primary_key=True, autoincrement=True)
    course_id    = Column(Integer, ForeignKey("courses.course_id"))
    day_of_week  = Column(String(10))   # e.g., "Monday"
    start_time   = Column(Time)
    end_time     = Column(Time)

    course = relationship("Course", back_populates="schedules")

    def __repr__(self):
        return f"<CourseSchedule(course={self.course_id}, day={self.day_of_week})>"


# ============================================================
# Create all tables in college_db_orm
# ============================================================
if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("All tables created in college_db_orm ✅")
