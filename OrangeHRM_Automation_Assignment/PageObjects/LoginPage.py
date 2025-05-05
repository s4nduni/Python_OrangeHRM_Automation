from selenium.webdriver.common.by import By

class Login:
    text_box_username_Name = "username"
    text_box_password_Name = "password"
    btn_login_xpath = '//*[@id="app"]/div[1]/div/div[1]/div/div[2]/div[2]/form/div[3]/button'

    def __init__(self, driver):
        self.driver = driver

    def setUsername(self, username):
        self.driver.find_element(By.NAME, self.text_box_username_Name).clear()
        self.driver.find_element(By.NAME, self.text_box_username_Name).send_keys(username)

    def setPassword(self, password):
        self.driver.find_element(By.NAME, self.text_box_password_Name).clear()
        self.driver.find_element(By.NAME, self.text_box_password_Name).send_keys(password)

    def clickLogin(self):
        self.driver.find_element(By.XPATH, self.btn_login_xpath).click()
