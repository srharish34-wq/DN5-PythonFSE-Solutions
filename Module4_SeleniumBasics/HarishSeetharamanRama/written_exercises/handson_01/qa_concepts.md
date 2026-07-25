# Hands-On 1: QA Concepts, Functional Testing & Defect Lifecycle

## Task 1: Map Testing Types to a Real System

### 1. Test cases per test level (Course Management API)

**Unit Testing** — test a single function in isolation
- Test: `validate_course_code(code)` function correctly rejects a course code longer than 10 characters.

**Integration Testing** — test two components working together
- Test: `POST /api/courses/` endpoint correctly writes a new course row into the database and the returned response matches the stored record.

**System Testing** — full end-to-end flow
- Test: A client sends `POST /api/courses/` with valid data → API validates → API writes to DB → API returns 201 with course ID → `GET /api/courses/{id}` returns the same data.

**User Acceptance Testing (UAT)** — from the perspective of an actual college admin
- Test: A college admin logs into the admin portal, creates a new course "Data Structures — CS201", and confirms it appears in the course listing exactly as entered, with no technical errors shown.

### 2. Functional vs Non-Functional Classification

| Test Case | Classification |
|---|---|
| Unit — validate_course_code rejects long codes | Functional |
| Integration — DB write matches response | Functional |
| System — full create-then-fetch flow | Functional |
| UAT — admin creates course via UI | Functional |

**Non-functional example:** Performance test — `POST /api/courses/` must respond within 300ms under normal load (answers "how well," not "does it work").

### 3. Black-Box vs White-Box Testing

- **Black-Box Testing:** Testing without knowledge of internal code — only inputs and expected outputs are known. Tester sends a request and checks the response against the spec.
- **White-Box Testing:** Testing with knowledge of internal code structure — paths, branches, and logic are tested directly (e.g., unit tests covering every `if` branch).

**Who performs which:** QA testers typically perform Black-Box testing (they validate behavior against requirements). Developers typically perform White-Box testing (they know and test the internal code paths, e.g., via unit tests).

### 4. Formal Test Cases — `POST /api/courses/`

| Test Case ID | Description | Preconditions | Test Steps | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|---|---|---|
| TC_COURSE_001 | Create course with valid data | API is running, DB is reachable, admin is authenticated | 1. Send POST with valid `{name, code, credits}`<br>2. Capture response | Response is `201 Created` with the created course object including a generated ID | | |
| TC_COURSE_002 | Reject duplicate course code | A course with code "CS201" already exists | 1. Send POST with `code="CS201"` again | Response is `400 Bad Request` with an error message stating the code already exists | | |
| TC_COURSE_003 | Reject missing required field | API is running | 1. Send POST with `name` missing | Response is `422 Unprocessable Entity` listing `name` as a required field | | |

---

## Task 2: Defect Lifecycle & Severity Classification

### 5. Defect Lifecycle

```
New → Assigned → Open → Fixed → Retest → Verified → Closed
                    │
                    ├── Rejected  (dev disagrees it's a bug / not reproducible)
                    └── Deferred  (valid bug, fix postponed to a later release)
```

- **New:** Defect logged by QA, not yet reviewed.
- **Assigned:** Triaged and assigned to a developer.
- **Open:** Developer has acknowledged and started work.
- **Fixed:** Developer has applied a fix and checked in code.
- **Retest:** QA re-executes the failed test case against the fix.
- **Verified:** QA confirms the fix resolves the issue.
- **Closed:** Defect lifecycle complete.
- **Rejected:** Developer determines it's not a valid defect (e.g., works as designed, cannot reproduce) — sent back to QA for confirmation or dispute.
- **Deferred:** Valid defect, but fix is postponed to a future release (e.g., low priority, release deadline).

### 6. Severity & Priority Classification

| Bug | Severity | Priority | Justification |
|---|---|---|---|
| a) POST /api/courses/ returns 500 for all requests | Critical | P1 | Core functionality completely broken for all users — blocks the entire feature. |
| b) Course names >150 chars silently truncated | Medium | P3 | Data integrity issue but doesn't crash the system or block usage; edge case. |
| c) Typo in Swagger `/docs` description | Low | P4 | Cosmetic only, no functional impact. |
| d) Intermittent 401 on correct login (first attempt) | High | P2 | Impacts core auth functionality and user trust, but not 100% reproducible — still urgent due to instability it signals. |

### 7. Defect Report — Bug (a)

| Field | Value |
|---|---|
| Defect ID | DEF-1042 |
| Title | POST /api/courses/ returns 500 Internal Server Error for all requests |
| Environment | Staging, Ubuntu 22.04, Python 3.11, PostgreSQL 15 |
| Build Version | v2.3.0-rc1 |
| Severity | Critical |
| Priority | P1 |
| Steps to Reproduce | 1. Authenticate as admin<br>2. Send `POST /api/courses/` with any valid payload<br>3. Observe response |
| Expected Result | `201 Created` with the new course object |
| Actual Result | `500 Internal Server Error`, no course created |
| Attachments | screenshot of 500 error |

### 8. Severity vs Priority

- **Severity** measures how badly the defect affects the system (functional impact).
- **Priority** measures how urgently it must be fixed (business/scheduling impact).

**Example where High Severity ≠ High Priority:** A crash in a rarely-used legacy report export feature (High Severity — the feature completely fails) might be Low Priority if that feature is being deprecated next release and almost no users touch it. Conversely, a cosmetic bug on the CEO's dashboard (Low Severity — nothing breaks) could be High Priority because of visibility and optics.
