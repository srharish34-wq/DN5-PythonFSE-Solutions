# ============================================================
# Hands-On 4 – Flask App Structure, Routing & Blueprints
# flask_coursemanager/app.py
# Cognizant DN5.0 | Harish Seetharaman Rama
# pip install flask flask-sqlalchemy flask-migrate
# Run: python app.py
# ============================================================

from flask import Flask, jsonify
from config import Config
from courses.routes import courses_bp


def create_app():
    """Application factory pattern — keeps app testable and avoids circular imports."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register blueprints
    app.register_blueprint(courses_bp)

    # ── JSON Error Handlers (APIs should NEVER return HTML errors) ──
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({
            'error': {
                'code': 'NOT_FOUND',
                'message': str(e)
            }
        }), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({
            'error': {
                'code': 'SERVER_ERROR',
                'message': 'An internal server error occurred'
            }
        }), 500

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
