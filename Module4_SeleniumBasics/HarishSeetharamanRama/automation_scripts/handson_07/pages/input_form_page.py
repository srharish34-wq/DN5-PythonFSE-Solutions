"""
HANDS-ON 7 | Task 2 (Step 57): InputFormPage — page object for the
Input Form Submit demo.

NOTE: confirmed via live DOM inspection - the real form fields are:
name, email, password, company, website, city, address_line1,
address_line2, state, zip (ALL marked required). There is no phone field
on this page - the earlier assumption of "phone"/"address" was wrong.
The id "inputEmail4" is used here because name="email" is NOT unique on
this page (a duplicate "email" field exists elsewhere in the site header).
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class InputFormPage(BasePage):
    NAME_INPUT = (By.NAME, "name")
    EMAIL_INPUT = (By.ID, "inputEmail4")
    PASSWORD_INPUT = (By.ID, "inputPassword4")
    COMPANY_INPUT = (By.NAME, "company")
    WEBSITE_INPUT = (By.NAME, "website")
    CITY_INPUT = (By.NAME, "city")
    ADDRESS1_INPUT = (By.NAME, "address_line1")
    ADDRESS2_INPUT = (By.NAME, "address_line2")
    STATE_INPUT = (By.ID, "inputState")
    ZIP_INPUT = (By.NAME, "zip")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button.selenium_btn")
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, "p.success-msg")

    def fill_form(self, name, email, password, company, website,
                  city, address1, address2, state, zip_code):
        self.wait_for_element(self.NAME_INPUT).send_keys(name)
        self.driver.find_element(*self.EMAIL_INPUT).send_keys(email)
        self.driver.find_element(*self.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*self.COMPANY_INPUT).send_keys(company)
        self.driver.find_element(*self.WEBSITE_INPUT).send_keys(website)
        self.driver.find_element(*self.CITY_INPUT).send_keys(city)
        self.driver.find_element(*self.ADDRESS1_INPUT).send_keys(address1)
        self.driver.find_element(*self.ADDRESS2_INPUT).send_keys(address2)
        self.driver.find_element(*self.STATE_INPUT).send_keys(state)
        self.driver.find_element(*self.ZIP_INPUT).send_keys(zip_code)

    def submit_form(self):
        self.wait_for_clickable(self.SUBMIT_BUTTON).click()

    def get_success_message(self) -> str:
        return self.wait_for_element(self.SUCCESS_MESSAGE).text