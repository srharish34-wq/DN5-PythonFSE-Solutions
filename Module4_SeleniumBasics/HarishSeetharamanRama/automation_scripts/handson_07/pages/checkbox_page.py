"""
HANDS-ON 7 | Task 1: CheckboxPage — page object for the Checkbox Demo.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckboxPage(BasePage):
    CHECKBOX_BY_INDEX = "(//input[@type='checkbox'])[{index}]"

    def _checkbox(self, index: int):
        locator = (By.XPATH, self.CHECKBOX_BY_INDEX.format(index=index))
        return self.wait_for_element(locator)

    def check_option(self, index: int):
        box = self._checkbox(index)
        if not box.is_selected():
            box.click()

    def uncheck_option(self, index: int):
        box = self._checkbox(index)
        if box.is_selected():
            box.click()

    def is_option_checked(self, index: int) -> bool:
        return self._checkbox(index).is_selected()
