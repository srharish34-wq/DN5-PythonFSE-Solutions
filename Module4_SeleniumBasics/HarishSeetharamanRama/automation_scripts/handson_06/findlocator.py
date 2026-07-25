"""
DIAGNOSTIC SCRIPT — run this once to find the real locator.
It opens the page, clicks Show Message, then prints the actual HTML
around the output area so we can write a correct, exact locator.

Run:
    python find_locator.py
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

options = Options()
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get("https://www.lambdatest.com/selenium-playground/")
    driver.find_element(By.LINK_TEXT, "Simple Form Demo").click()

    driver.find_element(By.ID, "user-message").send_keys("Hello Selenium")
    driver.find_element(By.ID, "showInput").click()

    time.sleep(2)  # give the page a moment to render the output

    # Print the HTML of the whole right-hand "Your Message:" panel.
    # We search for any element containing the text "Your Message"
    # and print its parent container's full HTML.
    try:
        label_el = driver.find_element(By.XPATH, "//*[contains(text(),'Your Message')]")
        parent = label_el.find_element(By.XPATH, "./..")
        grandparent = parent.find_element(By.XPATH, "./..")
        print("\n===== LABEL ELEMENT outerHTML =====")
        print(driver.execute_script("return arguments[0].outerHTML;", label_el))
        print("\n===== PARENT outerHTML =====")
        print(driver.execute_script("return arguments[0].outerHTML;", parent))
        print("\n===== GRANDPARENT outerHTML =====")
        print(driver.execute_script("return arguments[0].outerHTML;", grandparent))
    except Exception as e:
        print("Could not find 'Your Message' text on the page:", e)
        print("\n===== FULL PAGE SOURCE (first 5000 chars) =====")
        print(driver.page_source[:5000])

    input("\nPress Enter to close the browser...")

finally:
    driver.quit()