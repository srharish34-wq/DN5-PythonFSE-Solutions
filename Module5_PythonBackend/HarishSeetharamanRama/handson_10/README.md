# Hands-On 10 — Microservices Architecture

## Task 1: Service Decomposition

The Course Management API was decomposed into the following bounded contexts:

| Service Name | Responsibility | Endpoints it Owns | Database it Owns |
|---|---|---|---|
| **Course Service** (port 5001) | Department & Course CRUD | `/api/courses/*`, `/api/departments/*` | `course_service.db` |
| **Student Service** (port 5002) | Student CRUD, Enrollment logic | `/api/students/*` | `student_service.db` |
| **Auth Service** *(not implemented here — see handson_09)* | Registration, login, token validation | `/api/auth/*` | Users table |
| **Notification Service** *(simulated via background task in handson_07)* | Sending confirmation emails | N/A (event-driven) | None |

Each service:
- Owns its own SQLite database — no service queries another's DB directly
- Runs independently on its own port
- Communicates with other services only via HTTP (synchronous) calls

---

## Task 2: Architecture Diagram

```
                        ┌─────────────────┐
        Client  ───────▶│   API Gateway    │  (port 5000)
                        │  (single entry)  │
                        └────────┬─────────┘
                                 │
                 ┌───────────────┴───────────────┐
                 ▼                                ▼
        ┌─────────────────┐              ┌──────────────────┐
        │  Course Service  │              │  Student Service  │
        │   (port 5001)    │◀────HTTP─────│   (port 5002)     │
        │  course_service.db│   GET /api/  │ student_service.db│
        └─────────────────┘   courses/{id}│└──────────────────┘
```

When a client enrolls a student:
1. Request hits the **Gateway** (`POST /api/students/1/enroll`)
2. Gateway proxies to **Student Service**
3. Student Service calls **Course Service** via HTTP to verify the course exists
4. If Course Service is down → Student Service returns `503 Service Unavailable`
5. If course exists → enrollment is created and confirmed

---

## How to Run

```bash
# Terminal 1
cd course_service
pip install -r requirements.txt
python app.py
# → Running on http://localhost:5001

# Terminal 2
cd student_service
pip install -r requirements.txt
python app.py
# → Running on http://localhost:5002

# Terminal 3
cd gateway
pip install -r requirements.txt
python app.py
# → Running on http://localhost:5000
```

## Test the Full Flow

```bash
# Through the gateway:
curl -X POST http://localhost:5000/api/students/1/enroll \
  -H "Content-Type: application/json" \
  -d "{\"course_id\": 1}"

# Check gateway health (shows status of all services):
curl http://localhost:5000/health
```

To test the 503 failure scenario: stop Course Service (Ctrl+C in its terminal), then
try the enroll endpoint again — it will return `503 Service Unavailable`.

---

## Synchronous vs Asynchronous Trade-offs

See detailed comment block at the bottom of `gateway/app.py` for the full discussion
of HTTP vs Message Queue (RabbitMQ/Kafka) communication patterns.
