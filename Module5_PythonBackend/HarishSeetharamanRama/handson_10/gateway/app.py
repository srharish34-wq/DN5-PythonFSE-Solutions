# ============================================================
# Hands-On 10 – Microservices: API Gateway
# gateway/app.py
# Cognizant DN5.0 | Harish Seetharaman Rama
# pip install flask requests
# Run: python app.py  (runs on port 5000)
#
# This is a single entry point that proxies requests to the
# correct backend microservice — clients only ever talk to
# the Gateway, never directly to Course Service or Student Service.
# ============================================================

from flask import Flask, request, jsonify, Response
import requests
from requests.exceptions import ConnectionError

app = Flask(__name__)

# ── Service Registry (hardcoded here; in production this would
#    use service discovery like Consul, Eureka, or Kubernetes DNS) ──
SERVICES = {
    'courses' : 'http://localhost:5001',
    'students': 'http://localhost:5002',
}


def proxy_request(service_url, path):
    """
    Forwards the incoming request to the target microservice
    and relays back its response, status code, and headers.
    """
    url = f"{service_url}{path}"

    try:
        resp = requests.request(
            method  = request.method,
            url     = url,
            headers = {k: v for k, v in request.headers if k.lower() != 'host'},
            json    = request.get_json(silent=True),
            params  = request.args,
            timeout = 5
        )
    except ConnectionError:
        return jsonify({
            'error': f'Service at {service_url} is currently unavailable'
        }), 503

    return Response(
        resp.content,
        status      = resp.status_code,
        content_type= resp.headers.get('Content-Type', 'application/json')
    )


# ============================================================
# ROUTES — proxy everything under /api/courses/* and /api/students/*
# ============================================================

@app.route('/api/courses/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/api/courses/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def courses_proxy(path):
    """Routes everything under /api/courses/* → Course Service (port 5001)."""
    full_path = f"/api/courses/{path}" if path else "/api/courses/"
    return proxy_request(SERVICES['courses'], full_path)


@app.route('/api/students/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/api/students/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def students_proxy(path):
    """Routes everything under /api/students/* → Student Service (port 5002)."""
    full_path = f"/api/students/{path}" if path else "/api/students/"
    return proxy_request(SERVICES['students'], full_path)


@app.route('/health', methods=['GET'])
def gateway_health():
    """Check health of the Gateway and all downstream services."""
    statuses = {'gateway': 'healthy'}

    for name, url in SERVICES.items():
        try:
            r = requests.get(f"{url}/health", timeout=2)
            statuses[name] = 'healthy' if r.status_code == 200 else 'unhealthy'
        except ConnectionError:
            statuses[name] = 'unreachable'

    return jsonify(statuses)


if __name__ == '__main__':
    print("🚪 API Gateway running on http://localhost:5000")
    print("   Routes /api/courses/*  → Course Service  (5001)")
    print("   Routes /api/students/* → Student Service (5002)")
    app.run(debug=True, port=5000)


# ============================================================
# README NOTES (Task 2, Step 104)
# ============================================================
"""
TRADE-OFFS: Synchronous (HTTP) vs Asynchronous (Message Queue)
Inter-Service Communication

SYNCHRONOUS (HTTP — what we used here):
  Pros:
    - Simple to implement and debug
    - Immediate response/confirmation
    - Easy to test with Postman/curl
  Cons:
    - Tight coupling — if Course Service is down, enrollment FAILS
    - Caller blocks waiting for response (latency adds up)
    - Cascading failures possible if one service is slow

ASYNCHRONOUS (Message Queue — RabbitMQ/Kafka):
  Pros:
    - Services are decoupled — Student Service publishes an
      "EnrollmentRequested" event and doesn't wait for a response
    - Course Service processes the event whenever it's ready
    - If Course Service is down, the message queues up and
      gets processed once it's back online (resilience)
    - Better for high-throughput, eventual-consistency scenarios
  Cons:
    - More complex infrastructure (need to run RabbitMQ/Kafka)
    - Eventual consistency — enrollment may not be confirmed instantly
    - Harder to debug and trace request flow across services

WHEN TO USE A MESSAGE QUEUE:
  - High-volume events (e.g., thousands of enrollments per second)
  - When immediate confirmation isn't required (e.g., sending
    welcome emails, analytics events, notifications)
  - When you want services to be resilient to each other's downtime

WHEN TO USE SYNCHRONOUS HTTP:
  - When you need an immediate yes/no answer (e.g., "does this
    course exist?" before allowing enrollment)
  - Simple systems with few services
  - When strong consistency is more important than availability

A real API Gateway also handles authentication, rate limiting,
and SSL termination — this simple proxy only demonstrates the
routing concept without those production concerns.
"""
