"""
HANDS-ON 7 | Task 1: DropdownPage — page object for the Select Dropdown List demo.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage


class DropdownPage(BasePage):
    DAY_DROPDOWN = (By.ID, "select-demo")

    def select_day(self, day_name: str):
        dropdown_element = self.wait_for_element(self.DAY_DROPDOWN)
        select = Select(dropdown_element)
        select.select_by_visible_text(day_name)

    def get_selected_day(self) -> str:
        dropdown_element = self.wait_for_element(self.DAY_DROPDOWN)
        select = Select(dropdown_element)
        return select.first_selected_option.text
