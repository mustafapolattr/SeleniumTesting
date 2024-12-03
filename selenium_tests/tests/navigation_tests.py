from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from django.conf import settings


def test_navigation_to_pim():
    """Test navigation to the PIM page"""
    driver_path = settings.SELENIUM_DRIVER_PATH
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)

    try:
        driver.get(settings.ORANGEHRM_URL)
        driver.maximize_window()

        # Login first
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "username"))
        ).send_keys("Admin")

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "password"))
        ).send_keys("admin123")

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "orangehrm-login-button"))
        ).click()

        # Click on the PIM menu
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "PIM"))
        ).click()

        # Verify the PIM page is loaded
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "oxd-table-filter"))
        )
    finally:
        driver.quit()
