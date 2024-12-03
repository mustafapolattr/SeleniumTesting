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


def test_login_success():
    """Test login with correct credentials"""
    driver_path = settings.SELENIUM_DRIVER_PATH
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)

    try:
        driver.get(settings.ORANGEHRM_URL)
        driver.maximize_window()
        time.sleep(2)  # Wait for the page to load
        driver.save_screenshot(os.path.join(screenshot_dir, "login_page.png"))

        # Fill in the username field
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "username"))
        ).send_keys("Admin")
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshot_dir, "username_filled.png"))

        # Fill in the password field
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "password"))
        ).send_keys("admin123")
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshot_dir, "password_filled.png"))

        # Click the login button
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "orangehrm-login-button"))
        ).click()
        time.sleep(5)
        driver.save_screenshot(os.path.join(screenshot_dir, "dashboard_loaded.png"))

        # Verify the user is logged in by checking the presence of the profile picture
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "employee-image"))
        )
    finally:
        driver.quit()

def test_login_failure():
    """Test login with incorrect credentials"""
    driver_path = settings.SELENIUM_DRIVER_PATH
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)

    try:
        driver.get(settings.ORANGEHRM_URL)
        driver.maximize_window()
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshot_dir, "login_page.png"))

        # Fill in the username field with incorrect data
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "username"))
        ).send_keys("wrong_user")
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshot_dir, "username_filled_wrong.png"))

        # Fill in the password field with incorrect data
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "password"))
        ).send_keys("wrong_password")
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshot_dir, "password_filled_wrong.png"))

        # Click the login button
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "orangehrm-login-button"))
        ).click()
        time.sleep(5)
        driver.save_screenshot(os.path.join(screenshot_dir, "error_message_displayed.png"))

        # Verify the error message is displayed
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "oxd-alert-content-text"))
        )
    finally:
        driver.quit()


def test_login_empty_fields():
    """Test login with empty fields"""
    driver_path = settings.SELENIUM_DRIVER_PATH
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)

    try:
        driver.get(settings.ORANGEHRM_URL)
        driver.maximize_window()
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshot_dir, "login_page.png"))

        # Click the login button without filling any fields
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "orangehrm-login-button"))
        ).click()
        time.sleep(5)
        driver.save_screenshot(os.path.join(screenshot_dir, "required_fields_message.png"))

        # Verify the "Required" messages are displayed
        error_messages = WebDriverWait(driver, 10).until(
            lambda d: d.find_elements(By.CLASS_NAME, "oxd-input-field-error-message")
        )
        driver.save_screenshot(os.path.join(screenshot_dir, "error_messages_highlighted.png"))

        assert len(error_messages) == 2, "Both error messages not displayed!"
        assert error_messages[0].text == "Required", "Username error message is incorrect!"
        assert error_messages[1].text == "Required", "Password error message is incorrect!"
    finally:
        driver.quit()
