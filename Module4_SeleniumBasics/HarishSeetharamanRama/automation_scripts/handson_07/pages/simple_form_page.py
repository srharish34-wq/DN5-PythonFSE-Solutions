"""
HANDS-ON 7 | Task 1: SimpleFormPage — page object for the Simple Form Demo.
No assert statements here — only actions and return values (Step 52).

NOTE: the live site reuses the id "user-message" on both the actual
<input> textbox and the output wrapper <div>. By.ID would grab the wrong
element (Selenium always returns the first DOM match), so these locators
anchor to the visible label text instead, which is unique and reliable.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class SimpleFormPage(BasePage):
    # --- Step 51: class-level locator constants (never hardcode inline) ---
    MESSAGE_INPUT = (By.XPATH, "//label[text()='Enter Message']/following::input[1]")
    SUBMIT_BUTTON = (By.XPATH, "//button[contains(text(),'Get Checked Value')]")
    DISPLAYED_MESSAGE = (By.XPATH, "//label[contains(text(),'Your Message')]/following-sibling::p[@id='message']")

    def enter_message(self, text: str):
        field = self.wait_for_element(self.MESSAGE_INPUT)
        field.clear()
        field.send_keys(text)

    def click_submit(self):
        button = self.wait_for_clickable(self.SUBMIT_BUTTON)
        button.click()

    def get_displayed_message(self) -> str:
        # Poll until the <p id="message"> actually has non-empty text,
        # not just until it exists/is visible (it exists empty from page load).
        from selenium.webdriver.support.ui import WebDriverWait

        element = WebDriverWait(self.driver, 10).until(
            lambda d: d.find_element(*self.DISPLAYED_MESSAGE)
            if d.find_element(*self.DISPLAYED_MESSAGE).text.strip()
            else False
        )
        return element.text