# Hands-On 2: SDLC vs TDLC — V-Model & Agile QA Integration

## Task 1: V-Model Mapping

### 9. V-Model Diagram (ASCII)

```
Requirements                                   Acceptance Testing
      \                                              /
       System Design                    System Testing
             \                              /
              Architecture Design   Integration Testing
                    \                 /
                     Module Design  Unit Testing
                           \        /
                            Coding
                          (bottom vertex)
```

Left side = Development (SDLC), Right side = Testing (TDLC). Each left phase has a directly corresponding right phase at the same level.

### 10. SDLC Phase → Test Artifact Produced

| SDLC Phase | TDLC Phase (mirrored) | Test Artifact Produced |
|---|---|---|
| Requirements | Acceptance Testing | Acceptance Test Plan / Acceptance Criteria |
| System Design | System Testing | System Test Plan |
| Architecture Design | Integration Testing | Integration Test Plan |
| Module Design | Unit Testing | Unit Test Cases |
| Coding | — | Code + developer unit tests |

### 11. Entry & Exit Criteria per TDLC Phase

**Unit Testing**
- Entry: Code module is complete and compiles; unit test cases are written.
- Exit: All unit tests pass; code coverage meets the agreed threshold (e.g., 80%).

**Integration Testing**
- Entry: Individual units are unit-tested and available for integration; integration test plan is ready.
- Exit: All integration points tested; no critical/high defects open on interfaces.

**System Testing**
- Entry: Full application build is deployed to the test environment; integration testing is complete.
- Exit: All planned system test cases executed; defect count below threshold; no open critical/high defects.

**Acceptance Testing (UAT)**
- Entry: System testing is complete and signed off; UAT environment mirrors production.
- Exit: Business stakeholders approve the system meets acceptance criteria; sign-off obtained.

### 12. Early QA Engagement Points (Course Management API)

1. **Requirements Review:** QA reviews the user stories for the course creation feature before coding starts, catching ambiguous requirements (e.g., "what happens on duplicate course codes?") early.
2. **API Contract / Design Review:** QA reviews the proposed API schema (request/response shapes, status codes) during Architecture Design, before implementation, to ensure it's testable and consistent.

---

## Task 2: Agile QA and Shift-Left Testing

### 13. Problems with Waterfall Testing-After-Development

1. **Late defect discovery:** Bugs found only after full development are far more expensive to fix (design flaws may require rework of the whole architecture).
2. **Compressed testing timeline:** If development runs late, testing time is often the first thing cut, leading to a rushed, lower-quality test cycle.
3. **Requirements drift:** By the time testing starts, business needs may have changed, so what's tested no longer matches what's actually needed — requiring re-work.

### 14. QA in Agile Ceremonies

- **Sprint Planning:** QA helps define clear, testable Acceptance Criteria for each story before it's committed to the sprint.
- **Daily Standup:** QA reports blocking issues (e.g., environment down, a defect blocking further testing) so the team can act quickly.
- **Sprint Review:** QA demonstrates tested functionality to stakeholders, confirming it meets the acceptance criteria shown live.
- **Retrospective:** QA raises process improvements — e.g., recurring defect patterns, flaky test issues, or better ways to write acceptance criteria.

### 15. Shift-Left Practices (Course Management API)

(a) **Reviewing requirements for testability** — QA reviews each user story to confirm it has clear, verifiable acceptance criteria before development starts (e.g., "create course" story must specify exact validation rules).

(b) **Writing test cases before code (TDD/BDD)** — Developers write a failing unit test for `POST /api/courses/` validation logic before implementing it, ensuring the code is built to pass a known specification.

(c) **Static code analysis** — Tools like `pylint`/`flake8` run automatically on every commit to the Course Management API repo, catching code smells and potential bugs before manual testing even begins.

(d) **API contract testing before integration** — The API's OpenAPI/Swagger schema is validated against a contract test suite before the frontend team integrates, catching breaking changes early.

### 16. Acceptance Criteria — Given-When-Then

**User Story:** As a college admin, I want to create a new course, so that students can enroll in it.

```gherkin
Scenario: Happy path — successfully create a course
  Given I am logged in as a college admin
  When I submit a new course with a unique course code, valid name, and credit value
  Then the course is created successfully
  And I see the new course listed in the course catalog

Scenario: Duplicate course code
  Given a course with code "CS201" already exists
  When I try to create a new course with code "CS201"
  Then the system rejects the request
  And I see an error message stating the course code is already in use

Scenario: Missing required fields
  Given I am logged in as a college admin
  When I submit a new course without a course name
  Then the system rejects the request
  And I see an error message indicating "name" is required
```
