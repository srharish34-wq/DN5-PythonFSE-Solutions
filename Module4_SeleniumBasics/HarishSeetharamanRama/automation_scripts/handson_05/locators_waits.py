"""
HANDS-ON 5 | Locators — ID, Name, XPath, CSS Selectors & Explicit Waits
==========================================================================
Task 1: Locator Strategies — From Simple to Robust
Task 2: WebDriverWait and Expected Conditions

Run directly:
    python locators_waits.py

NOTE: Exact ID/class/name attribute values depend on the live LambdaTest
Selenium Playground HTML. Inspect via DevTools (F12) first and adjust any
locator values marked <<INSPECT>> if the site markup has changed.
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

PLAYGROUND_URL = "https://www.lambdatest.com/selenium-playground/"


def build_driver(headless: bool = False):
    options = Options()
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)
    return driver


# ==========================================================================
# TASK 1: Locator Strategies — From Simple to Robust
# ==========================================================================

def task1_locator_strategies_demo():
    """Step 32 & 33: locate the same element 6 ways, then 3 CSS variants."""
    driver = build_driver(headless=False)
    try:
        driver.get(PLAYGROUND_URL)
        driver.find_element(By.LINK_TEXT, "Simple Form Demo").click()

        # --- Step 32: Six locator strategies for the message input field ---

        # 1. By ID  (<<INSPECT>> confirm actual id, e.g. "user-message")
        el_by_id = driver.find_element(By.ID, "user-message")
        print("By.ID found:", el_by_id.is_displayed())

        # 2. By NAME
        el_by_name = driver.find_element(By.NAME, "message")
        print("By.NAME found:", el_by_name.is_displayed())

        # 3. By CLASS_NAME
        el_by_class = driver.find_element(By.CLASS_NAME, "form-control")
        print("By.CLASS_NAME found:", el_by_class.is_displayed())

        # 4. By TAG_NAME (locate the <input> tag within the form container)
        form_container = driver.find_element(By.CLASS_NAME, "form-group")
        el_by_tag = form_container.find_element(By.TAG_NAME, "input")
        print("By.TAG_NAME found:", el_by_tag.is_displayed())

        # 5. By XPATH — absolute path (fragile, for demonstration only)
        el_by_abs_xpath = driver.find_element(
            By.XPATH, "/html/body/div[2]/div/div[2]/div[1]/div/div[2]/div/form/div[1]/input"
        )
        print("By.XPATH (absolute) found:", el_by_abs_xpath.is_displayed())

        # 6. By XPATH — relative path using attributes (robust)
        el_by_rel_xpath = driver.find_element(By.XPATH, "//input[@id='user-message']")
        print("By.XPATH (relative) found:", el_by_rel_xpath.is_displayed())

        # --- Step 33: three CSS selector variants for the same element ---
        css_by_id = driver.find_element(By.CSS_SELECTOR, "#user-message")
        css_by_attr = driver.find_element(By.CSS_SELECTOR, "[name='message']")
        css_by_parent_child = driver.find_element(By.CSS_SELECTOR, "div.form-group > input")
        print(
            "CSS selectors all found:",
            css_by_id.is_displayed(),
            css_by_attr.is_displayed(),
            css_by_parent_child.is_displayed(),
        )

    finally:
        driver.quit()


def task1_checkbox_text_xpath_demo():
    """Step 34: XPath with text() and contains()."""
    driver = build_driver(headless=False)
    try:
        driver.get(PLAYGROUND_URL)
        driver.find_element(By.LINK_TEXT, "Checkbox Demo").click()

        first_option = driver.find_element(By.XPATH, "//label[text()='Option 1']")
        print("First checkbox label found via text():", first_option.text)

        all_options = driver.find_elements(By.XPATH, "//label[contains(text(),'Option')]")
        print(f"Found {len(all_options)} labels containing 'Option'")
        for opt in all_options:
            print(" -", opt.text)

    finally:
        driver.quit()


# --- Step 35: Locator ranking, most to least preferred ---
LOCATOR_RANKING = """
Ranking (most -> least preferred) for maintainable automation:

1. ID              - Unique per element (by spec), fastest lookup, very readable,
                      rarely changes unless the dev deliberately renames it.
2. NAME             - Usually unique within a form, readable, fairly stable.
3. CSS_SELECTOR     - Fast, flexible, supports attributes/parent-child relations,
                      generally faster to evaluate than XPath in most browsers.
4. XPATH (relative, attribute-based e.g. //input[@id='x'])
                    - Powerful (supports text(), contains(), axes like parent/
                      ancestor) but slightly slower than CSS and easier to write
                      badly.
5. CLASS_NAME / TAG_NAME
                    - Classes are often shared by many elements (styling classes),
                      making them non-unique and brittle; tag name alone almost
                      never uniquely identifies a single element.
6. XPATH (absolute, e.g. /html/body/div[2]/div/...)
                    - LEAST preferred. Breaks with ANY structural HTML change
                      (an extra wrapping <div> anywhere breaks the whole path).
                      Not human-readable, hard to maintain.

Justification: uniqueness and stability matter most for maintainability -
IDs and names are least likely to change and are explicit developer contracts
with automation/accessibility tools. Absolute XPath encodes the entire DOM
structure, so it is the most brittle to any front-end change.
"""


# ==========================================================================
# TASK 2: WebDriverWait and Expected Conditions
# ==========================================================================

def task2_explicit_wait_alert_demo():
    """Step 36: wait for success alert to be visible, assert text."""
    driver = build_driver(headless=False)
    try:
        driver.get(PLAYGROUND_URL)
        driver.find_element(By.LINK_TEXT, "Bootstrap Alerts").click()

        driver.find_element(By.ID, "success-alert").click()

        alert_div = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
        )
        assert "successfully" in alert_div.text.lower(), (
            f"Expected 'successfully' in alert text, got: {alert_div.text}"
        )
        print("Alert text assertion passed:", alert_div.text)
    finally:
        driver.quit()


def task2_sleep_vs_explicit_wait_timing_demo():
    """Step 37: compare time.sleep(3) vs explicit wait for the same action."""
    # --- Version A: time.sleep(3) ---
    driver = build_driver(headless=False)
    try:
        driver.get(PLAYGROUND_URL)
        driver.find_element(By.LINK_TEXT, "Bootstrap Alerts").click()
        start = time.time()
        driver.find_element(By.ID, "success-alert").click()
        time.sleep(3)  # BAD PRACTICE: always waits the full 3s, even if ready sooner
        alert = driver.find_element(By.CSS_SELECTOR, ".alert-success")
        assert alert.is_displayed()
        print(f"[sleep(3)] elapsed: {time.time() - start:.2f}s")
    finally:
        driver.quit()

    # --- Version B: explicit wait ---
    driver = build_driver(headless=False)
    try:
        driver.get(PLAYGROUND_URL)
        driver.find_element(By.LINK_TEXT, "Bootstrap Alerts").click()
        start = time.time()
        driver.find_element(By.ID, "success-alert").click()
        alert = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".alert-success"))
        )
        assert alert.is_displayed()
        print(f"[explicit wait] elapsed: {time.time() - start:.2f}s")
    finally:
        driver.quit()

    # COMMENT (Step 37): On a fast machine, the explicit-wait version finishes
    # almost immediately once the condition is true (often well under 1s),
    # while time.sleep(3) ALWAYS burns the full 3 seconds regardless of how
    # fast the element actually appeared. On a slow machine/network, sleep(3)
    # might not even be long enough (causing a flaky failure), whereas the
    # explicit wait keeps polling up to its timeout and succeeds reliably.
    # => explicit waits are both faster on average AND more reliable.


def task2_clickable_wait_demo():
    """Step 38: wait for element to be clickable before clicking."""
    driver = build_driver(headless=False)
    try:
        driver.get(PLAYGROUND_URL)
        driver.find_element(By.LINK_TEXT, "Bootstrap Alerts").click()

        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "success-alert"))
        )
        button.click()
        # NOTE (Step 38): visibility_of_element_located only checks that the
        # element exists in the DOM AND has a non-zero size (i.e., you could
        # SEE it). element_to_be_clickable checks all of that PLUS that the
        # element is enabled (not disabled) and not obscured by another
        # element on top of it (e.g., a loading spinner or modal overlay).
        # A button can be visible but still not clickable (e.g., disabled
        # while a form validates, or covered by an overlay) — clickable is
        # the stricter, safer condition to wait for before calling .click().
        print("Clicked using element_to_be_clickable wait")
    finally:
        driver.quit()


def task2_fluent_wait_demo():
    """Step 39: FluentWait - poll every 500ms, timeout 10s, ignore NoSuchElementException."""
    driver = build_driver(headless=False)
    try:
        driver.get(PLAYGROUND_URL)
        driver.find_element(By.LINK_TEXT, "Table Sort").click()

        fluent_wait = WebDriverWait(
            driver,
            timeout=10,
            poll_frequency=0.5,
            ignored_exceptions=[NoSuchElementException],
        )

        row = fluent_wait.until(
            lambda d: d.find_element(By.CSS_SELECTOR, "table tbody tr")
        )
        print("Dynamically-loaded table row found:", row.text)
    finally:
        driver.quit()


if __name__ == "__main__":
    task1_locator_strategies_demo()
    task1_checkbox_text_xpath_demo()
    print(LOCATOR_RANKING)

    task2_explicit_wait_alert_demo()
    task2_sleep_vs_explicit_wait_timing_demo()
    task2_clickable_wait_demo()
    task2_fluent_wait_demo()
