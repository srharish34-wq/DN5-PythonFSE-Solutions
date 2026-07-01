# ============================================================
# Hands-On 5 – Flask SQLAlchemy Models
# models.py
# Cognizant DN5.0 | Harish Seetharaman Rama
# ============================================================

from app import db


class Department(db.Model):
    __tablename__ = 'departments'

    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(100), nullable=False)
    head_of_dept = db.Column(db.String(100))
    budget       = db.Column(db.Numeric(12, 2))

    courses  = db.relationship('Course',  back_populates='department', lazy=True)
    students = db.relationship('Student', back_populates='department', lazy=True)

    def to_dict(self):
        return {
            'id'          : self.id,
            'name'        : self.name,
            'head_of_dept': self.head_of_dept,
            'budget'      : float(self.budget) if self.budget else None
        }

    def __repr__(self):
        return f'<Department {self.name}>'


class Course(db.Model):
    __tablename__ = 'courses'

    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(150), nullable=False)
    code          = db.Column(db.String(20), unique=True, nullable=False)
    credits       = db.Column(db.Integer)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))

    department  = db.relationship('Department', back_populates='courses')
    enrollments = db.relationship('Enrollment', back_populates='course', lazy=True)

    def to_dict(self):
        return {
            'id'             : self.id,
            'name'           : self.name,
            'code'           : self.code,
            'credits'        : self.credits,
            'department_id'  : self.department_id,
            'department_name': self.department.name if self.department else None
        }

    def __repr__(self):
        return f'<Course {self.code}>'


class Student(db.Model):
    __tablename__ = 'students'

    id              = db.Column(db.Integer, primary_key=True)
    first_name      = db.Column(db.String(50), nullable=False)
    last_name       = db.Column(db.String(50), nullable=False)
    email           = db.Column(db.String(100), unique=True, nullable=False)
    department_id   = db.Column(db.Integer, db.ForeignKey('departments.id'))
    enrollment_year = db.Column(db.Integer)

    department  = db.relationship('Department', back_populates='students')
    enrollments = db.relationship('Enrollment', back_populates='student', lazy=True)

    def to_dict(self):
        return {
            'id'             : self.id,
            'first_name'     : self.first_name,
            'last_name'      : self.last_name,
            'email'          : self.email,
            'department_id'  : self.department_id,
            'enrollment_year': self.enrollment_year
        }

    def __repr__(self):
        return f'<Student {self.first_name} {self.last_name}>'


class Enrollment(db.Model):
    __tablename__ = 'enrollments'

    id              = db.Column(db.Integer, primary_key=True)
    student_id      = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    course_id       = db.Column(db.Integer, db.ForeignKey('courses.id'),  nullable=False)
    enrollment_date = db.Column(db.Date,    nullable=False)
    grade           = db.Column(db.String(2))

    student = db.relationship('Student', back_populates='enrollments')
    course  = db.relationship('Course',  back_populates='enrollments')

    __table_args__ = (
        db.UniqueConstraint('student_id', 'course_id', name='uq_student_course'),
    )

    def to_dict(self):
        return {
            'id'             : self.id,
            'student_id'     : self.student_id,
            'course_id'      : self.course_id,
            'enrollment_date': str(self.enrollment_date),
            'grade'          : self.grade
        }

    def __repr__(self):
        return f'<Enrollment student={self.student_id} course={self.course_id}>'