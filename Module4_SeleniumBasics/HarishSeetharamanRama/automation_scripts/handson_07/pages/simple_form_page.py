"""
HANDS-ON 7 | Task 1: SimpleFormPage — page object for the Simple Form Demo.
No assert statements here — only actions and return values (Step 52).

NOTE on locators (confirmed via live DOM inspection):
- The live site reuses the id "user-message" on THREE elements: the real
  <input>, an output wrapper <div> for "Your Message:", and another output
  wrapper <div> for "Result:" (Two Input Fields section). We locate the
  input by its unique placeholder text instead.
- The "Enter Message" text is a <p> tag, not a <label>.
- The output text lives in a uniquely-scoped <p id="message">.
- This page appears to use client-side routing; interacting with the form
  immediately after navigation can race against the page still rendering.
  navigate_to() here waits for the input to be present, then adds a short
  settle delay before returning control to the caller.
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class SimpleFormPage(BasePage):
    # --- Step 51: class-level locator constants (never hardcode inline) ---
    MESSAGE_INPUT = (By.CSS_SELECTOR, "input[placeholder='Please enter your Message']")
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(text(),'Get Checked Value')]")
    DISPLAYED_MESSAGE = (By.XPATH, "//label[contains(text(),'Your Message')]/following-sibling::p[@id='message']")

    def wait_until_ready(self):
        """Call this right after navigating here — waits for the form to
        be present and gives the page a moment to finish rendering."""
        self.wait_for_element(self.MESSAGE_INPUT)
        time.sleep(1)

    def enter_message(self, text: str):
        # Re-find the field fresh (avoids a stale element reference if the
        # page re-rendered after wait_until_ready()).
        field = self.driver.find_element(*self.MESSAGE_INPUT)
        field.click()
        field.clear()
        field.send_keys(text)

    def click_submit(self):
        button = self.wait_for_clickable(self.SUBMIT_BUTTON)
        button.click()

    def get_displayed_message(self) -> str:
        # Poll until the <p id="message"> actually has non-empty text,
        # not just until it exists/is visible (it exists empty from page load).
        element = WebDriverWait(self.driver, 10).until(
            lambda d: d.find_element(*self.DISPLAYED_MESSAGE)
            if d.find_element(*self.DISPLAYED_MESSAGE).text.strip()
            else False
        )
        return element.text