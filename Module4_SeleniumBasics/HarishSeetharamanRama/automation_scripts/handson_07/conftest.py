"""
HANDS-ON 7 | conftest.py — fixtures for the POM-structured test suite.
Lives at handson_07/conftest.py so it's shared by everything under tests/.
"""

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="session")
def base_url():
    return "https://www.lambdatest.com/selenium-playground/"


@pytest.fixture(scope="function")
def driver():
    options = Options()
    # options.add_argument("--headless=new")  # uncomment for CI/headless runs
    options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=options)
    drv.implicitly_wait(5)

    yield drv

    drv.quit()
