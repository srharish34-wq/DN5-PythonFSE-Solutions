"""
HANDS-ON 6 | Task 1 & 2: pytest tests for the LambdaTest Selenium Playground.

Run:
    pytest test_playground.py -v
    pytest test_playground.py --html=report.html --self-contained-html

NOTE on locators (confirmed via live DOM inspection):
- The live site reuses the id "user-message" on the real <input>, an
  output wrapper <div> for "Your Message:", AND another output wrapper
  <div> for "Result:" (Two Input Fields section) — three elements, same id.
  We locate the input by its unique placeholder text instead.
- The "Enter Message" text is a <p> tag, not a <label>.
- The output text lives in a uniquely-scoped <p id="message">.
- After clicking the "Simple Form Demo" nav link, we wait briefly for the
  page to settle before typing, since this appears to be a client-side
  routed page and typing too early (right after navigation) can race
  against the page finishing its render.
"""

import time
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

MESSAGE_INPUT_LOCATOR = (By.CSS_SELECTOR, "input[placeholder='Please enter your Message']")
SHOW_MESSAGE_BUTTON_XPATH = "//button[contains(text(),'Get Checked Value')]"
MESSAGE_OUTPUT_XPATH = "//label[contains(text(),'Your Message')]/following-sibling::p[@id='message']"


def _open_simple_form_demo(driver, base_url):
    driver.get(base_url)
    driver.find_element(By.LINK_TEXT, "Simple Form Demo").click()
    # Let the (likely client-side-routed) page finish rendering before
    # interacting, to avoid racing against React/JS hydration.
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(MESSAGE_INPUT_LOCATOR)
    )
    time.sleep(1)


def _submit_message_and_get_result(driver, message: str) -> str:
    """Type message, click, wait for non-empty result. Self-diagnosing:
    dumps debug info (including browser console logs) before re-raising
    if it still times out."""
    # Re-find the input fresh right before typing (avoid a stale element
    # reference if the page re-rendered after our initial wait).
    message_input = driver.find_element(*MESSAGE_INPUT_LOCATOR)
    message_input.click()
    message_input.clear()
    message_input.send_keys(message)

    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, SHOW_MESSAGE_BUTTON_XPATH))
    )
    button.click()

    try:
        displayed_message = WebDriverWait(driver, 10).until(
            lambda d: d.find_element(By.XPATH, MESSAGE_OUTPUT_XPATH)
            if d.find_element(By.XPATH, MESSAGE_OUTPUT_XPATH).text.strip()
            else False
        )
        return displayed_message.text
    except Exception:
        print("\n===== DEBUG: input value at time of failure =====")
        try:
            print(repr(driver.find_element(*MESSAGE_INPUT_LOCATOR).get_attribute("value")))
        except Exception as e:
            print("could not read input value:", e)
        print("\n===== DEBUG: elements with id='message' =====")
        for el in driver.find_elements(By.ID, "message"):
            print(driver.execute_script("return arguments[0].outerHTML;", el))
        print("\n===== DEBUG: browser console logs =====")
        try:
            for entry in driver.get_log("browser"):
                print(entry)
        except Exception as e:
            print("could not read browser logs:", e)
        raise


# --- Step 40 & 42: simple form submission test ---
def test_simple_form_submission(driver, base_url):
    _open_simple_form_demo(driver, base_url)
    result_text = _submit_message_and_get_result(driver, "Hello Selenium")
    assert result_text == "Hello Selenium"


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
    _open_simple_form_demo(driver, base_url)
    result_text = _submit_message_and_get_result(driver, message)
    assert result_text == message


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
@pytest.mark.skip(reason="demo only - unskip to verify the failure screenshot hook works")
def test_intentional_failure_for_screenshot_demo(driver, base_url):
    driver.get(base_url)
    assert driver.title == "This Will Never Match"