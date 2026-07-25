"""
HANDS-ON 7 | Task 2: Full POM-refactored test suite.

Run (from the handson_07/ folder):
    pytest tests/ -v --html=report.html --self-contained-html

Golden rule of POM: THIS file contains assertions (what should happen).
Page classes (in pages/) contain interactions (how to make it happen).
There are ZERO driver.find_element calls in this file — verify with:
    grep -r "find_element" tests/test_pom_suite.py   (should return nothing)
"""

from selenium.webdriver.common.by import By
from pages.simple_form_page import SimpleFormPage
from pages.checkbox_page import CheckboxPage
from pages.dropdown_page import DropdownPage
from pages.input_form_page import InputFormPage


# --- Step 55: Simple Form test refactored to POM ---
def test_simple_form_submission(driver, base_url):
    page = SimpleFormPage(driver)
    page.navigate_to(base_url)
    driver.find_element(By.LINK_TEXT, "Simple Form Demo").click()

    page.enter_message("Hello Selenium")
    page.click_submit()

    assert page.get_displayed_message() == "Hello Selenium"


# --- Step 56: Checkbox test refactored to POM ---
def test_checkbox_demo(driver, base_url):
    driver.get(base_url)
    driver.find_element(By.LINK_TEXT, "Checkbox Demo").click()

    page = CheckboxPage(driver)
    page.check_option(1)
    assert page.is_option_checked(1) is True

    page.uncheck_option(1)
    assert page.is_option_checked(1) is False


# --- Step 56: Dropdown test refactored to POM ---
def test_dropdown_selection(driver, base_url):
    driver.get(base_url)
    driver.find_element(By.LINK_TEXT, "Select Dropdown List").click()

    page = DropdownPage(driver)
    page.select_day("Wednesday")

    assert page.get_selected_day() == "Wednesday"


# --- Step 57: new Input Form Submit test using InputFormPage ---
def test_input_form_submit(driver, base_url):
    driver.get(base_url)
    driver.find_element(By.LINK_TEXT, "Input Form Submit").click()

    page = InputFormPage(driver)
    page.fill_form(
        name="Jane Doe",
        email="jane.doe@example.com",
        phone="9876543210",
        address="221B Baker Street",
    )
    page.submit_form()

    assert "success" in page.get_success_message().lower()


# --- Step 59: maintenance benefit explanation ---
"""
If the Submit button's ID changed from 'submit' to 'btn-submit' in a FLAT
(non-POM) script, every single test file that directly called
driver.find_element(By.ID, 'submit') would break, and a developer would need
to hunt down and fix EVERY occurrence across the whole test suite - easy to
miss one and leave a silently broken test.

With POM, the locator is defined ONCE as a class-level constant inside the
relevant page class (e.g., SimpleFormPage.SUBMIT_BUTTON). When the ID changes,
only that ONE line in ONE file needs to be updated. Every test that uses
page.click_submit() automatically picks up the fix with zero changes to any
test file. This is the core maintenance benefit of the Page Object Model:
it isolates UI changes to a single, predictable location instead of letting
them ripple across the entire test suite.
"""
