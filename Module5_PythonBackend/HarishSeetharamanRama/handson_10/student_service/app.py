# ============================================================
# Hands-On 10 – Microservices: Student Service
# student_service/app.py
# Cognizant DN5.0 | Harish Seetharaman Rama
# pip install flask flask-sqlalchemy requests
# Run: python app.py  (runs on port 5002)
# ============================================================

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import requests
from requests.exceptions import ConnectionError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student_service.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

COURSE_SERVICE_URL = 'http://localhost:5001'


# ── Student Service owns ONLY student & enrollment data ────
# It does NOT have direct access to the Course Service's database.
# To verify a course exists, it must call Course Service over HTTP.

class Student(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    first_name      = db.Column(db.String(50), nullable=False)
    last_name       = db.Column(db.String(50), nullable=False)
    email           = db.Column(db.String(100), unique=True, nullable=False)
    enrollment_year = db.Column(db.Integer)

    def to_dict(self):
        return {'id': self.id, 'first_name': self.first_name,
                'last_name': self.last_name, 'email': self.email,
                'enrollment_year': self.enrollment_year}


class Enrollment(db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    student_id      = db.Column(db.Integer, db.ForeignKey('student.id'))
    course_id       = db.Column(db.Integer)  # Reference only — no FK to another service's DB!
    enrollment_date = db.Column(db.Date)

    def to_dict(self):
        return {'id': self.id, 'student_id': self.student_id,
                'course_id': self.course_id,
                'enrollment_date': str(self.enrollment_date)}


# ============================================================
# ROUTES
# ============================================================

@app.route('/api/students/', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([s.to_dict() for s in students])


@app.route('/api/students/', methods=['POST'])
def create_student():
    data = request.get_json()
    if not data or not all(k in data for k in ['first_name', 'last_name', 'email']):
        return jsonify({'error': 'Missing required fields'}), 400

    student = Student(
        first_name      = data['first_name'],
        last_name       = data['last_name'],
        email           = data['email'],
        enrollment_year = data.get('enrollment_year')
    )
    db.session.add(student)
    db.session.commit()
    return jsonify(student.to_dict()), 201


@app.route('/api/students/<int:student_id>/enroll', methods=['POST'])
def enroll_student(student_id):
    """
    TASK 2 (Hands-On 10): Inter-service communication.

    This endpoint calls Course Service's GET /api/courses/{id}/
    to verify the course exists BEFORE creating the enrollment.
    """
    from datetime import date

    student = Student.query.get(student_id)
    if not student:
        return jsonify({'error': f'Student {student_id} not found'}), 404

    data = request.get_json()
    course_id = data.get('course_id') if data else None
    if not course_id:
        return jsonify({'error': 'course_id is required'}), 400

    # ── Call Course Service over HTTP to verify the course exists ──
    try:
        response = requests.get(
            f"{COURSE_SERVICE_URL}/api/courses/{course_id}/",
            timeout=3
        )
    except ConnectionError:
        # Course Service is down — handle gracefully
        return jsonify({
            'error': 'Course Service is currently unavailable. Please try again later.'
        }), 503

    if response.status_code == 404:
        return jsonify({'error': f'Course {course_id} does not exist'}), 404

    course_data = response.json()

    # Create the enrollment
    enrollment = Enrollment(
        student_id      = student_id,
        course_id       = course_id,
        enrollment_date = date.today()
    )
    db.session.add(enrollment)
    db.session.commit()

    return jsonify({
        'enrollment': enrollment.to_dict(),
        'course'    : course_data  # data fetched from Course Service
    }), 201


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'service': 'student_service', 'status': 'healthy'})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if Student.query.count() == 0:
            db.session.add_all([
                Student(first_name='Arjun', last_name='Mehta',
                        email='arjun@college.edu', enrollment_year=2022),
                Student(first_name='Priya', last_name='Suresh',
                        email='priya@college.edu', enrollment_year=2022),
            ])
            db.session.commit()

    print("🚀 Student Service running on http://localhost:5002")
    app.run(debug=True, port=5002)
