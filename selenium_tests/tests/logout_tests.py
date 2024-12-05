import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from django.conf import settings

project_root = os.path.dirname(os.path.abspath(__file__))
screenshot_dir = os.path.join(project_root, "../../screenshots")

if not os.path.exists(screenshot_dir):
    os.makedirs(screenshot_dir)


def test_logout():
    """Test user logout functionality"""
    driver_path = settings.SELENIUM_DRIVER_PATH
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)

    try:
        # Login to the system
        driver.get(settings.ORANGEHRM_URL)
        driver.maximize_window()
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshot_dir, "logout_login_page.png"))

        # Fill in the username field
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "username"))
        ).send_keys("Admin")
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshot_dir, "logout_username_filled.png"))

        # Fill in the password field
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "password"))
        ).send_keys("admin123")
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshot_dir, "logout_password_filled.png"))

        # Click the login button
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "orangehrm-login-button"))
        ).click()
        time.sleep(5)
        driver.save_screenshot(os.path.join(screenshot_dir, "logout_dashboard_loaded.png"))

        # Click the profile icon
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "oxd-userdropdown-name"))
        ).click()
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshot_dir, "logout_dropdown_opened.png"))

        # Click the logout button
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Logout')]"))
        ).click()
        time.sleep(5)
        driver.save_screenshot(os.path.join(screenshot_dir, "logout_login_screen.png"))

        # Verify user is redirected to the login page
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
    finally:
        driver.quit()
