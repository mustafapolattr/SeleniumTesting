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


def test_navigation():
    """Test navigation through main menu items"""
    driver_path = settings.SELENIUM_DRIVER_PATH
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)

    try:
        # Login to the system
        driver.get(settings.ORANGEHRM_URL)
        driver.maximize_window()
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshot_dir, "navigation_login_page.png"))

        # Fill in the username field
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "username"))
        ).send_keys("Admin")
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshot_dir, "navigation_username_filled.png"))

        # Fill in the password field
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.NAME, "password"))
        ).send_keys("admin123")
        time.sleep(2)
        driver.save_screenshot(os.path.join(screenshot_dir, "navigation_password_filled.png"))

        # Click the login button
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "orangehrm-login-button"))
        ).click()
        time.sleep(5)
        driver.save_screenshot(os.path.join(screenshot_dir, "navigation_dashboard_loaded.png"))

        # Navigate to Admin page
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Admin']"))
        ).click()
        time.sleep(5)
        driver.save_screenshot(os.path.join(screenshot_dir, "navigation_admin_page.png"))

        # Navigate to PIM page
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='PIM']"))
        ).click()
        time.sleep(5)
        driver.save_screenshot(os.path.join(screenshot_dir, "navigation_pim_page.png"))

        # Navigate to Leave page
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Leave']"))
        ).click()
        time.sleep(5)
        driver.save_screenshot(os.path.join(screenshot_dir, "navigation_leave_page.png"))

        # Verify that we are still logged in and on a valid page
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "oxd-topbar-header-title"))
        )
    finally:
        driver.quit()
