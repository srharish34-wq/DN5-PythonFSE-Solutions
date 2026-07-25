"""
DIAGNOSTIC SCRIPT #2 — finds the real "Enter Message" input field HTML.
Run:
    python find_input.py
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

options = Options()
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.get("https://www.lambdatest.com/selenium-playground/")
    driver.find_element(By.LINK_TEXT, "Simple Form Demo").click()

    inputs = driver.find_elements(By.TAG_NAME, "input")
    print(f"\nFound {len(inputs)} <input> elements on the page:\n")
    for i, el in enumerate(inputs):
        html = driver.execute_script("return arguments[0].outerHTML;", el)
        print(f"--- input[{i}] ---")
        print(html)
        print()

    try:
        label_el = driver.find_element(By.XPATH, "//*[contains(text(),'Enter Message')]")
        parent = label_el.find_element(By.XPATH, "./..")
        print("\n===== 'Enter Message' LABEL outerHTML =====")
        print(driver.execute_script("return arguments[0].outerHTML;", label_el))
        print("\n===== 'Enter Message' PARENT outerHTML =====")
        print(driver.execute_script("return arguments[0].outerHTML;", parent))
    except Exception as e:
        print("Could not find 'Enter Message' text:", e)

    driver.get("https://www.lambdatest.com/selenium-playground/checkbox-demo")
    checkboxes = driver.find_elements(By.XPATH, "//input[@type='checkbox']")
    print(f"\nFound {len(checkboxes)} checkboxes. First checkbox is_selected() = {checkboxes[0].is_selected() if checkboxes else 'N/A'}")

    input("\nPress Enter to close the browser...")

finally:
    driver.quit()