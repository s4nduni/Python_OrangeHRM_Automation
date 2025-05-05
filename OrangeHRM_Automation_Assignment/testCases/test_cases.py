import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from PageObjects.LeavePage import LeavePage
from PageObjects.LoginPage import Login
from PageObjects.DashboardPage import Dashboard
import os
import allure


class Test_001_OrangeHRM:
    base_url = "https://opensource-demo.orangehrmlive.com/web/index.php/auth/login"
    username = "Admin"
    password = "admin123"

    # Get the absolute path of the current file
    current_file_path = os.path.abspath(__file__)

    # Go up one directory to get tests directory
    testCases_dir = os.path.dirname(current_file_path)

    # Go up one more directory to get project root
    project_root = os.path.dirname(testCases_dir)

    # Define screenshots directory at project root level
    screenshots_dir = os.path.join(project_root, "Screenshots")

    @pytest.fixture(autouse=True)
    def setup(self):
        # Print current paths for debugging
        print(f"Current file path: {self.current_file_path}")
        print(f"Tests directory: {self.testCases_dir}")
        print(f"Project root: {self.project_root}")
        print(f"Screenshots directory: {self.screenshots_dir}")

        # Create Screenshots directory if it doesn't exist
        os.makedirs(self.screenshots_dir, exist_ok=True)

        self.driver = webdriver.Chrome()
        self.driver.get(self.base_url)
        self.driver.maximize_window()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        yield
        self.driver.quit()

    def test_login_page_title(self):
        """Test to verify the Home page title """
        # Take screenshot with a simple name
        screenshot_path = os.path.join(self.screenshots_dir, "login_title_test.png")
        print(f"Saving screenshot to: {screenshot_path}")

        try:
            result = self.driver.save_screenshot(screenshot_path)
            print(f"Screenshot saved successfully: {result}, exists: {os.path.exists(screenshot_path)}")
        except Exception as e:
            print(f"Error taking screenshot: {str(e)}")

        # Continue with the actual test
        assert self.driver.title == "OrangeHRM"

    def test_login_functionality(self):
        """Test to verify the log functionality"""
        login = Login(self.driver)
        login.setUsername(self.username)
        login.setPassword(self.password)
        login.clickLogin()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//h6[text()="Dashboard"]'))
        )
        assert "dashboard" in self.driver.current_url

        # Take direct screenshot after successful login
        screenshot_path = os.path.join(self.screenshots_dir, "successful_login.png")
        print(f"Saving screenshot to: {screenshot_path}")
        self.driver.save_screenshot(screenshot_path)

    def test_leave_functionality(self):
        """Test to verify the leave functionality"""
        # Log in to the application
        login = Login(self.driver)
        login.setUsername(self.username)
        login.setPassword(self.password)
        login.clickLogin()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//h6[text()="Dashboard"]'))
        )

        # Click on the "My Leave" button using the title attribute
        dashboard = Dashboard(self.driver)

        # Assuming the button has the title attribute with value "My Leave"
        my_leave_button_xpath = "//button[@title='My Leave']"

        # Wait for the button to be clickable and click it
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, my_leave_button_xpath))
        ).click()

        # Wait for the leave page to load and the necessary element to appear
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "oxd-layout")]'))
        )

        # Optionally, check if the page header contains 'Leave'
        leave_page = LeavePage(self.driver)
        header_text = leave_page.get_leave_header()

        print(f"Header text found: '{header_text}'")

        # Take screenshot at this point
        screenshot_path = os.path.join(self.screenshots_dir, "leave_page.png")
        print(f"Saving screenshot to: {screenshot_path}")
        self.driver.save_screenshot(screenshot_path)

        # If the header text is 'Leave', it indicates the "My Leave" page is loaded
        assert header_text, "No header text found - element not located"
        assert "Leave" in header_text, f"Expected 'Leave' in header but got: '{header_text}'"

    def test_logout_functionality(self):
        """Test to verify the logout functionality"""
        login = Login(self.driver)
        login.setUsername(self.username)
        login.setPassword(self.password)
        login.clickLogin()
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//h6[text()="Dashboard"]'))
        )

        dashboard = Dashboard(self.driver)
        dashboard.clickProfileDropdown()
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//a[text()='Logout']"))
        )
        dashboard.clickLogout()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        # Take screenshot at this point
        screenshot_path = os.path.join(self.screenshots_dir, "logout_complete.png")
        print(f"Saving screenshot to: {screenshot_path}")
        self.driver.save_screenshot(screenshot_path)

        assert "auth/login" in self.driver.current_url

    # Hook for handling failed tests
    @pytest.hookimpl(hookwrapper=True, tryfirst=True)
    def pytest_runtest_makereport(item, call):
        outcome = yield
        rep = outcome.get_result()

        # Only take screenshot for failed tests
        if rep.when == "call" and not rep.passed:
            driver = getattr(item.instance, "driver", None)
            if driver:
                try:
                    # Get the screenshots directory from the test class
                    test_class = item.instance.__class__
                    if hasattr(test_class, "screenshots_dir"):
                        # Create a Failed subfolder in the screenshots directory
                        failed_dir = os.path.join(test_class.screenshots_dir, "Failed")
                        os.makedirs(failed_dir, exist_ok=True)

                        screenshot_path = os.path.join(failed_dir, f"{item.name}_failed.png")
                        driver.save_screenshot(screenshot_path)
                        print(f"Saved failure screenshot to {screenshot_path}")
                except Exception as e:
                    print(f"Error saving failure screenshot: {str(e)}")