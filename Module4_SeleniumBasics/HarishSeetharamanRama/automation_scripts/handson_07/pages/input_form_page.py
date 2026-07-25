"""
HANDS-ON 7 | Task 2 (Step 57): InputFormPage — page object for the
Input Form Submit demo (name, email, phone, address fields).
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class InputFormPage(BasePage):
    NAME_INPUT = (By.NAME, "name")
    EMAIL_INPUT = (By.NAME, "inputEmail4")
    PHONE_INPUT = (By.NAME, "phone")
    ADDRESS_INPUT = (By.NAME, "address")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "input.btn.btn-primary")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".success-msg, .alert-success")

    def fill_form(self, name: str, email: str, phone: str, address: str):
        self.wait_for_element(self.NAME_INPUT).send_keys(name)
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)
        self.driver.find_element(*self.PHONE_INPUT).send_keys(phone)
        self.driver.find_element(*self.ADDRESS_INPUT).send_keys(address)

    def submit_form(self):
        self.wait_for_clickable(self.SUBMIT_BUTTON).click()

    def get_success_message(self) -> str:
        return self.wait_for_element(self.SUCCESS_MESSAGE).text
