"""
HANDS-ON 7 | Task 1: CheckboxPage — page object for the Checkbox Demo.

NOTE: methods operate on a WebElement reference obtained via get_checkbox()
rather than re-querying by index on every call. Re-querying by index was
found to be unreliable here (the checkbox list appears to re-render after
interaction, which can shift what a given index refers to) - holding a
single element reference across the whole check/uncheck sequence, the way
a human interacting with one checkbox naturally would, avoids that.
"""

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckboxPage(BasePage):
    CHECKBOX_BY_INDEX = "(//input[@type='checkbox'])[{index}]"

    def get_checkbox(self, index: int):
        """Fetch the checkbox once; reuse the returned element for all
        subsequent actions on it instead of re-querying by index."""
        locator = (By.XPATH, self.CHECKBOX_BY_INDEX.format(index=index))
        return self.wait_for_element(locator)

    def check_option(self, checkbox):
        if not checkbox.is_selected():
            checkbox.click()

    def uncheck_option(self, checkbox):
        if checkbox.is_selected():
            checkbox.click()

    def is_option_checked(self, checkbox) -> bool:
        return checkbox.is_selected()