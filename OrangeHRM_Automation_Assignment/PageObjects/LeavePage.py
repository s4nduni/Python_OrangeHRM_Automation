from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class LeavePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # Multiple possible locators for the header
    LEAVE_HEADER_LOCATORS = [
        (By.XPATH, '//h5[contains(., "Leave")]'),  # Try h5 first
        (By.XPATH, '//h6[contains(., "Leave")]'),  # Then try h6
        (By.XPATH, '//*[contains(@class, "oxd-text") and contains(., "Leave")]'),  # More generic
        (By.XPATH, '//div[contains(@class, "orangehrm-header")]//*[contains(., "Leave")]')
    ]

    def get_leave_header(self):
        for locator in self.LEAVE_HEADER_LOCATORS:
            try:
                element = self.wait.until(EC.visibility_of_element_located(locator))
                return element.text
            except:
                continue
        return ""