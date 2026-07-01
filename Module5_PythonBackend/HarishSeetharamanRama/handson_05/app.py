from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///coursemanager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Department(db.Model):
    __tablename__ = 'departments'
    id           = db.Column(db.Integer, primary_key=True)
    name         = db.Column(db.String(100), nullable=False)
    head_of_dept = db.Column(db.String(100))
    budget       = db.Column(db.Numeric(12, 2))
    def to_dict(self):
        return {'id': self.id, 'name': self.name}

class Course(db.Model):
    __tablename__ = 'courses'
    id            = db.Column(db.Integer, primary_key=True)
    name          = db.Column(db.String(150), nullable=False)
    code          = db.Column(db.String(20), unique=True, nullable=False)
    credits       = db.Column(db.Integer)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    def to_dict(self):
        return {'id': self.id, 'name': self.name,
                'code': self.code, 'credits': self.credits,
                'department_id': self.department_id}

class Student(db.Model):
    __tablename__ = 'students'
    id              = db.Column(db.Integer, primary_key=True)
    first_name      = db.Column(db.String(50), nullable=False)
    last_name       = db.Column(db.String(50), nullable=False)
    email           = db.Column(db.String(100), unique=True, nullable=False)
    enrollment_year = db.Column(db.Integer)
    def to_dict(self):
        return {'id': self.id, 'first_name': self.first_name,
                'last_name': self.last_name, 'email': self.email}

class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    id              = db.Column(db.Integer, primary_key=True)
    student_id      = db.Column(db.Integer, db.ForeignKey('students.id'))
    course_id       = db.Column(db.Integer, db.ForeignKey('courses.id'))
    enrollment_date = db.Column(db.Date)
    grade           = db.Column(db.String(2))
    def to_dict(self):
        return {'id': self.id, 'student_id': self.student_id,
                'course_id': self.course_id, 'grade': self.grade}

with app.app_context():
    db.create_all()

@app.route('/api/courses/', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    return jsonify([c.to_dict() for c in courses])

@app.route('/api/courses/', methods=['POST'])
def create_course():
    data = request.get_json()
    if not data or not all(k in data for k in ['name','code','credits']):
        return jsonify({'error': 'Missing required fields'}), 400
    course = Course(name=data['name'], code=data['code'],
                    credits=data['credits'],
                    department_id=data.get('department_id'))
    db.session.add(course)
    db.session.commit()
    return jsonify(course.to_dict()), 201

@app.route('/api/courses/<int:id>/', methods=['GET'])
def get_course(id):
    course = Course.query.get_or_404(id)
    return jsonify(course.to_dict())

@app.route('/api/courses/<int:id>/', methods=['PUT'])
def update_course(id):
    course = Course.query.get_or_404(id)
    data = request.get_json()
    course.name    = data.get('name',    course.name)
    course.code    = data.get('code',    course.code)
    course.credits = data.get('credits', course.credits)
    db.session.commit()
    return jsonify(course.to_dict())

@app.route('/api/courses/<int:id>/', methods=['DELETE'])
def delete_course(id):
    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    return jsonify({}), 204

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5000)