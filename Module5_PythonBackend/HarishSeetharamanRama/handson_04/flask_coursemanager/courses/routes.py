# ============================================================
# Hands-On 4 – Flask Blueprint Routes
# flask_coursemanager/courses/routes.py
# Cognizant DN5.0 | Harish Seetharaman Rama
# ============================================================

from flask import Blueprint, jsonify, request

# Blueprint — Flask's way of organising routes into modules (like Django apps but lighter)
courses_bp = Blueprint('courses', __name__, url_prefix='/api/courses')

# In-memory store for Hands-On 4 (replaced with DB in Hands-On 5)
courses_db = []
next_id    = 1


def make_response_json(data, status_code=200):
    """Helper: consistent JSON envelope for all responses."""
    return jsonify({'status': 'success', 'data': data}), status_code


# ── GET /api/courses/ ──────────────────────────────────────
@courses_bp.route('/', methods=['GET'])
def get_courses():
    return make_response_json(courses_db)


# ── POST /api/courses/ ────────────────────────────────────
@courses_bp.route('/', methods=['POST'])
def create_course():
    global next_id
    data = request.get_json()

    # Validate required fields — return 400 if any missing
    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400

    required = ['name', 'code', 'credits']
    missing  = [f for f in required if f not in data]
    if missing:
        return jsonify({
            'error': f"Missing required fields: {', '.join(missing)}"
        }), 400

    course = {
        'id'         : next_id,
        'name'       : data['name'],
        'code'       : data['code'],
        'credits'    : data['credits'],
        'department' : data.get('department', None),
    }
    courses_db.append(course)
    next_id += 1

    response = make_response_json(course, 201)
    return response


# ── GET /api/courses/<id>/ ────────────────────────────────
@courses_bp.route('/<int:course_id>/', methods=['GET'])
def get_course(course_id):
    course = next((c for c in courses_db if c['id'] == course_id), None)
    if not course:
        return jsonify({'error': f'Course with id {course_id} not found'}), 404
    return make_response_json(course)


# ── PUT /api/courses/<id>/ ───────────────────────────────
@courses_bp.route('/<int:course_id>/', methods=['PUT'])
def update_course(course_id):
    course = next((c for c in courses_db if c['id'] == course_id), None)
    if not course:
        return jsonify({'error': f'Course with id {course_id} not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400

    course.update({
        'name'      : data.get('name',       course['name']),
        'code'      : data.get('code',       course['code']),
        'credits'   : data.get('credits',    course['credits']),
        'department': data.get('department', course['department']),
    })
    return make_response_json(course)


# ── DELETE /api/courses/<id>/ ────────────────────────────
@courses_bp.route('/<int:course_id>/', methods=['DELETE'])
def delete_course(course_id):
    global courses_db
    course = next((c for c in courses_db if c['id'] == course_id), None)
    if not course:
        return jsonify({'error': f'Course with id {course_id} not found'}), 404

    courses_db = [c for c in courses_db if c['id'] != course_id]
    return jsonify({}), 204
