# Hands-On 3: Test Automation Process, Lifecycle & Framework Types

## Task 1: Automation Decision and Test Case Selection

### 17. Five Criteria for Deciding Automation

Applied to: *"Test that POST /api/courses/ returns 201 with the correct course data when valid input is provided."*

1. **Repetitiveness** — Is this test run often (e.g., every build)? → Yes, this is a core regression test run on every deploy. Good candidate.
2. **Stability** — Is the feature's behavior stable (unlikely to change often)? → Yes, course creation is a core, stable endpoint. Good candidate.
3. **High business risk** — Does failure have serious consequences? → Yes, course creation is central to the product. Good candidate.
4. **Data-driven potential** — Can it be run with many input variations cheaply? → Yes, many valid input combinations can be tested via parameterization.
5. **ROI (time saved vs. effort to automate)** — Manual execution takes a few minutes each time; over dozens of runs, automation clearly pays off.

**Conclusion:** Strong candidate for automation.

### 18. Automate or Manual?

| Test Case | Decision | Justification |
|---|---|---|
| a) Regression for all CRUD endpoints after every code change | **Automate** | Repetitive, runs on every change — ideal automation candidate. |
| b) Exploratory testing of a new search feature | **Manual** | Exploratory testing relies on human intuition and creativity; not scriptable. |
| c) Performance test: 100 concurrent users on GET /api/courses/ | **Automate** (specialized tool, e.g. Locust/JMeter, not Selenium) | Needs to be repeated regularly and can't be done manually at scale. |
| d) UI test for the login form | **Automate** | Stable, repetitive, high-risk (auth) — good Selenium candidate. |
| e) Verify Swagger docs are accurate | **Manual** | Requires human judgment to assess accuracy/clarity of descriptions. |
| f) Smoke test: API reachable after deployment | **Automate** | Runs on every deployment; simple pass/fail check — ideal for CI pipeline automation. |

### 19. Automation ROI Calculation

- Automating: 4 hours (one-time)
- Manual run: 30 minutes (0.5 hours) each time
- Maintenance overhead: 20% extra time per run, *after the 10th run*

**Break-even without maintenance overhead:**
`4 hours / 0.5 hours per manual run = 8 runs` to break even.

**With maintenance overhead after run 10:**
- Runs 1–10: automated cost per run ≈ 0 (just execution, effectively free vs. manual)
- From run 11 onward: each automated run costs `20% × 0.5hr manual-equivalent = 0.1 hr` maintenance overhead
- By run 10, automation has already saved: `10 × 0.5hr = 5 hours` of manual effort against a 4-hour build cost → **already paid off around run 8**, with 2 extra runs of pure savings before overhead kicks in.

**Conclusion:** The automation pays for itself at **8 runs**, and remains net-positive even after the 20% maintenance overhead begins at run 11, since each automated run (even with overhead) still costs far less than the 30-minute manual alternative.

### 20. Flaky Tests

**Definition:** A flaky test is one that sometimes passes and sometimes fails *without any code change* — its result is inconsistent/non-deterministic.

**Example:** A Selenium test that clicks "Submit" and immediately checks for a success message, but the message takes variable time to render — the test passes when the network is fast and fails when it's slow.

**3 Strategies to Prevent/Fix Flaky Tests:**
1. Replace hard-coded `time.sleep()` with explicit `WebDriverWait` + `ExpectedConditions`.
2. Ensure test data isolation — each test creates and cleans up its own data instead of depending on shared/mutable state.
3. Avoid asserting on exact timing or animation states; wait for a stable, well-defined condition (e.g., element visible and enabled) instead of "the page probably loaded by now."

---

## Task 2: Compare Automation Framework Types

### 21. Framework Comparison

**Linear (Record & Playback)**
- Description: Tests are recorded step-by-step (often via a tool) with no reusable functions — each script is self-contained and hardcodes steps and data.
- Advantage: Very fast to create for simple, one-off tests; no coding skill required.
- Disadvantage: Not maintainable — any UI change requires re-recording every affected script.
- Example use: Quick smoke-check of a single, rarely-changing page.

**Modular**
- Description: Common actions (e.g., "login") are broken into reusable functions/modules that test scripts call.
- Advantage: Reduces duplication; a change to the login flow is fixed in one place.
- Disadvantage: Still requires programming knowledge; test data is often still hardcoded.
- Example use: A suite of tests that all need to log in first — login is a shared module.

**Data-Driven**
- Description: Test logic is separated from test data — the same script runs multiple times with different data sets (e.g., from CSV/Excel).
- Advantage: Easily test many input combinations without duplicating scripts.
- Disadvantage: Requires a mechanism to manage external data files; script complexity increases.
- Example use: Testing course creation with 50 different valid/invalid course name inputs.

**Keyword-Driven**
- Description: Test steps are represented as "keywords" (e.g., "Click", "EnterText") in a table/spreadsheet, interpreted by a driver engine — testers with minimal coding skill can write tests.
- Advantage: Non-technical team members can write and read tests.
- Disadvantage: Significant upfront investment to build the keyword engine/framework.
- Example use: A team with manual testers who need to contribute automated test cases without deep coding skills.

**Hybrid**
- Description: Combines Modular (reusable functions), Data-Driven (external test data), and optionally Keyword-Driven concepts into one framework.
- Advantage: Gets the benefits of all approaches — reusable, data-driven, and often accessible to less-technical testers.
- Disadvantage: More complex to design and maintain initially.
- Example use: A full-scale Selenium suite for the Course Management frontend used by both developers and manual QA.

### 22. Recommended Framework for the Given Scenario

**Scenario:** Login with 50 user/password combos, reuse login steps across 20 tests, support technical + non-technical testers.

**Recommendation: Hybrid Framework** (Modular + Data-Driven, with light Keyword-Driven elements)
- **Modular** covers reusing the login flow across 20 test cases (one login function/page object).
- **Data-Driven** covers running the 50 user/password combinations against that one login flow.
- Combining with a **Page Object Model** on top gives non-technical testers readable, business-language test steps (e.g., `login_page.login(user, password)`), lowering the barrier for less technical team members.

### 23. Hybrid Framework Folder Structure

```
CourseManagement-Frontend-Tests/
├── config/
│   └── config.yaml              # base_url, browser, timeouts, environment settings
├── data/
│   ├── login_credentials.csv    # 50 user/password combinations
│   └── course_test_data.json
├── pages/
│   ├── base_page.py
│   ├── login_page.py
│   └── course_page.py
├── tests/
│   ├── test_login.py
│   └── test_course_creation.py
├── utils/
│   ├── driver_factory.py        # creates/configures WebDriver instances
│   └── data_reader.py           # reads CSV/JSON test data
├── conftest.py                  # pytest fixtures (driver, base_url)
├── requirements.txt
└── pytest.ini
```
