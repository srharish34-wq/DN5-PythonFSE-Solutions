# ============================================================
# Hands-On 10 – Microservices: Course Service
# course_service/app.py
# Cognizant DN5.0 | Harish Seetharaman Rama
# pip install flask flask-sqlalchemy
# Run: python app.py  (runs on port 5001)
# ============================================================

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///course_service.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# ── Course Service owns ONLY course & department data ──────
# Key microservices principle: each service owns its data.
# No service should directly query another service's database.

class Department(db.Model):
    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(100), nullable=False)
    head_of_dept = db.Column(db.String(100))
    budget       = db.Column(db.Numeric(12, 2))

    def to_dict(self):
        return {'id': self.id, 'name': self.name,
                'head_of_dept': self.head_of_dept,
                'budget': float(self.budget) if self.budget else None}


class Course(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(150), nullable=False)
    code          = db.Column(db.String(20), unique=True, nullable=False)
    credits       = db.Column(db.Integer)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'code': self.code,
                'credits': self.credits, 'department_id': self.department_id}


# ============================================================
# ROUTES — Course Service owns these endpoints
# ============================================================

@app.route('/api/courses/', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify([c.to_dict() for c in courses])


@app.route('/api/courses/', methods=['POST'])
def create_course():
    data = request.get_json()
    if not data or not all(k in data for k in ['name', 'code', 'credits']):
        return jsonify({'error': 'Missing required fields'}), 400

    course = Course(
        name          = data['name'],
        code          = data['code'],
        credits       = data['credits'],
        department_id = data.get('department_id')
    )
    db.session.add(course)
    db.session.commit()
    return jsonify(course.to_dict()), 201


@app.route('/api/courses/<int:course_id>/', methods=['GET'])
def get_course(course_id):
    """This endpoint is called by Student Service to verify a course exists."""
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'error': f'Course {course_id} not found'}), 404
    return jsonify(course.to_dict())


@app.route('/api/departments/', methods=['GET'])
def get_departments():
    departments = Department.query.all()
    return jsonify([d.to_dict() for d in departments])


@app.route('/health', methods=['GET'])
def health_check():
    """Used by API Gateway / orchestrators to check service is alive."""
    return jsonify({'service': 'course_service', 'status': 'healthy'})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Seed some sample data if empty
        if Course.query.count() == 0:
            d1 = Department(name='Computer Science', head_of_dept='Dr. Ramesh', budget=850000)
            db.session.add(d1)
            db.session.commit()
            db.session.add_all([
                Course(name='Data Structures', code='CS101', credits=4, department_id=d1.id),
                Course(name='DBMS',            code='CS102', credits=3, department_id=d1.id),
            ])
            db.session.commit()

    print("🚀 Course Service running on http://localhost:5001")
    app.run(debug=True, port=5001)
