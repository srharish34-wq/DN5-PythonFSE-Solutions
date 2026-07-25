"""
HANDS-ON 6 | Task 1 & 2: pytest tests for the LambdaTest Selenium Playground.

Run:
    pytest test_playground.py -v
    pytest test_playground.py --html=report.html --self-contained-html

NOTE on locators: the live site reuses the id "user-message" on BOTH the
actual <input> textbox AND the output wrapper <div> that displays the
result. Relying on By.ID for that field grabs the wrong element, since
Selenium always returns the FIRST DOM match for a given id. To avoid this,
we anchor to the visible label text instead ("Enter Message" / "Your
Message:"), which is unique and unambiguous regardless of duplicate ids.
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

MESSAGE_INPUT_XPATH = "//label[text()='Enter Message']/following::input[1]"
SHOW_MESSAGE_BUTTON_XPATH = "//button[contains(text(),'Get Checked Value')]"
MESSAGE_OUTPUT_XPATH = "//label[contains(text(),'Your Message')]/following-sibling::p[@id='message']"


# --- Step 40 & 42: simple form submission test ---
def test_simple_form_submission(driver, base_url):
    driver.get(base_url)
    driver.find_element(By.LINK_TEXT, "Simple Form Demo").click()

    message_input = driver.find_element(By.XPATH, MESSAGE_INPUT_XPATH)
    message_input.send_keys("Hello Selenium")
    driver.find_element(By.XPATH, SHOW_MESSAGE_BUTTON_XPATH).click()

    displayed_message = WebDriverWait(driver, 10).until(
        lambda d: d.find_element(By.XPATH, MESSAGE_OUTPUT_XPATH)
        if d.find_element(By.XPATH, MESSAGE_OUTPUT_XPATH).text.strip()
        else False
    )
    assert displayed_message.text == "Hello Selenium"


# --- Step 40 & 43: checkbox interaction test ---
def test_checkbox_demo(driver, base_url):
    driver.get(base_url)
    driver.find_element(By.LINK_TEXT, "Checkbox Demo").click()

    first_checkbox = driver.find_element(By.XPATH, "(//input[@type='checkbox'])[1]")

    initial_state = first_checkbox.is_selected()

    first_checkbox.click()
    assert first_checkbox.is_selected() is not initial_state

    first_checkbox.click()
    assert first_checkbox.is_selected() is initial_state


# --- Step 45: parameterised form submission test (3 separate runs) ---
@pytest.mark.parametrize("message", ["Hello", "Selenium Automation", "12345"])
def test_simple_form_submission_parametrised(driver, base_url, message):
    driver.get(base_url)
    driver.find_element(By.LINK_TEXT, "Simple Form Demo").click()

    message_input = driver.find_element(By.XPATH, MESSAGE_INPUT_XPATH)
    message_input.send_keys(message)
    driver.find_element(By.XPATH, SHOW_MESSAGE_BUTTON_XPATH).click()

    displayed_message = WebDriverWait(driver, 10).until(
        lambda d: d.find_element(By.XPATH, MESSAGE_OUTPUT_XPATH)
        if d.find_element(By.XPATH, MESSAGE_OUTPUT_XPATH).text.strip()
        else False
    )
    assert displayed_message.text == message


# --- Step 49: dropdown selection test ---
def test_dropdown_selection(driver, base_url):
    driver.get(base_url)
    driver.find_element(By.LINK_TEXT, "Select Dropdown List").click()

    dropdown_element = driver.find_element(By.ID, "select-demo")
    select = Select(dropdown_element)
    select.select_by_visible_text("Wednesday")

    selected_option = select.first_selected_option
    assert selected_option.text == "Wednesday"


# --- Intentional failing test to demonstrate the screenshot-on-failure hook ---
# Unskip this temporarily to verify conftest.py's pytest_runtest_makereport
# hook actually captures a screenshot on failure (Step 46).
@pytest.mark.skip(reason="demo only - unskip to verify the failure screenshot hook works")
def test_intentional_failure_for_screenshot_demo(driver, base_url):
    driver.get(base_url)
    assert driver.title == "This Will Never Match"