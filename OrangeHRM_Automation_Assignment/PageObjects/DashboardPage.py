from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Dashboard:
    def __init__(self, driver):
        self.driver = driver
        self.link_my_leave = (By.XPATH, "//div[@class='orangehrm-quick-launch']//p[text()='My Leave']")
        self.profile_dropdown = (By.CLASS_NAME, "oxd-userdropdown-name")
        self.logout_link = (By.XPATH, "//a[text()='Logout']")

    def clickProfileDropdown(self):
        self.driver.find_element(*self.profile_dropdown).click()

    def clickLogout(self):
        self.driver.find_element(*self.logout_link).click()

    def clickMyLeave(self):
        try:
            leave_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//p[normalize-space()='My Leave']"))
            )
            leave_btn.click()
        except Exception as e:
            print("Failed to click 'My Leave'. Error:", e)
            self.driver.save_screenshot("click_my_leave_failed.png")
            raise
