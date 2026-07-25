"""
HANDS-ON 4 | Selenium WebDriver Setup, Browser Drivers & Basic Commands
==========================================================================
Task 1: Selenium Architecture and Environment Setup
Task 2: WebDriver Navigation and Window Commands

Run directly:
    python setup_test.py

Install first:
    pip install selenium webdriver-manager
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

PLAYGROUND_URL = "https://www.lambdatest.com/selenium-playground/"


# ==========================================================================
# TASK 1: Selenium Architecture and Environment Setup
# ==========================================================================
"""
Step 24 — Selenium Architecture — 3 main components:

1. WebDriver:
   The core component that directly communicates with the browser.
   Each browser (Chrome, Firefox, Edge) has its own driver executable
   (e.g., chromedriver.exe) that implements the W3C WebDriver protocol.
   Your Python script sends commands (e.g., "find this element", "click it")
   as HTTP requests to the driver, which translates them into native browser
   automation calls. This is a direct connection between script and browser.

2. Selenium Grid:
   Solves the problem of running tests in PARALLEL across multiple machines
   and/or multiple browser/OS combinations. Instead of running all tests
   sequentially on one machine, Grid distributes execution across a "hub"
   (coordinator) and multiple "nodes" (machines running actual browsers).
   This drastically reduces total test suite execution time and enables
   cross-browser/cross-platform testing at scale.

3. Selenium IDE:
   A browser extension (Chrome/Firefox) that RECORDS user interactions
   (clicks, typing, navigation) as you perform them, then PLAYS them back
   later. It can also export the recorded steps as code (e.g., Python +
   pytest). Useful for quickly prototyping a test flow or for testers with
   limited coding experience, though generated code usually needs cleanup
   (better locators, waits, assertions) before it's production-quality.
"""


def build_driver(headless: bool = False):
    """Step 25: Create and return a configured Chrome WebDriver instance
    using webdriver-manager (auto-downloads the matching ChromeDriver)."""
    options = Options()

    # Step 27: headless mode toggle
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Step 26: implicit wait
    driver.implicitly_wait(10)
    # NOTE (Step 26): Setting a global implicit wait is considered bad
    # practice because it applies the SAME wait time to every find_element()
    # call in the entire script — even when an element is expected
    # immediately (wasting time only on failures), or when a specific
    # element genuinely needs a longer/shorter wait than others (implicit
    # wait can't be tuned per-element). It can also interact unpredictably
    # when mixed with explicit waits, sometimes causing wait times to stack.
    # Explicit waits (WebDriverWait + ExpectedConditions, covered in
    # Hands-On 5) let you wait for a SPECIFIC condition on a SPECIFIC
    # element with a tailored timeout, which is far more reliable.

    return driver


def task1_open_and_print_title():
    """Step 25: open Chrome, navigate, print title, close browser."""
    driver = build_driver(headless=False)
    try:
        driver.get(PLAYGROUND_URL)
        print("Page title:", driver.title)
    finally:
        driver.quit()


def task1_headless_verification():
    """Step 27: run in headless mode, verify title still prints correctly."""
    driver = build_driver(headless=True)
    try:
        driver.get(PLAYGROUND_URL)
        print("Headless page title:", driver.title)
    finally:
        driver.quit()


# ==========================================================================
# TASK 2: WebDriver Navigation and Window Commands
# ==========================================================================

def task2_navigation_and_windows():
    driver = build_driver(headless=False)
    try:
        # --- Step 28: navigate to Simple Form Demo, assert URL, go back ---
        driver.get(PLAYGROUND_URL)
        simple_form_link = driver.find_element(By.LINK_TEXT, "Simple Form Demo")
        simple_form_link.click()

        assert "simple-form-demo" in driver.current_url, (
            f"Expected 'simple-form-demo' in URL, got: {driver.current_url}"
        )
        print("URL assertion passed:", driver.current_url)

        driver.back()
        print("Navigated back to:", driver.current_url)

        # --- Step 29: open a new tab, switch to it, print title ---
        driver.execute_script('window.open("https://www.google.com");')
        all_tabs = driver.window_handles
        print("Open tabs:", all_tabs)

        driver.switch_to.window(all_tabs[1])
        time.sleep(1)  # allow the new tab to finish loading its title
        print("New tab title:", driver.title)

        # --- Step 30: switch back to original tab, take screenshot ---
        driver.switch_to.window(all_tabs[0])
        driver.save_screenshot("playground_screenshot.png")
        print("Screenshot saved: playground_screenshot.png")

        # --- Step 31: get/set window size ---
        size = driver.get_window_size()
        print("Current window size:", size)

        driver.set_window_size(1280, 800)
        print("Window resized to 1280x800")
        # NOTE (Step 31): Consistent window size matters for responsive UI
        # automation because many pages change layout, hide/collapse menus,
        # or reflow elements at different breakpoints (mobile/tablet/
        # desktop). If window size varies between test runs, an element
        # that's visible and clickable at one size might be hidden behind a
        # hamburger menu or pushed off-screen at another, causing flaky,
        # environment-dependent test failures unrelated to any real bug.

    finally:
        driver.quit()


if __name__ == "__main__":
    task1_open_and_print_title()
    task1_headless_verification()
    task2_navigation_and_windows()
