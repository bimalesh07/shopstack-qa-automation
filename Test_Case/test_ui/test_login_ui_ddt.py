import pytest
import time
import json
from selenium.webdriver.common.by import By
from Utilities.customLogger import LogGen
from PageObjects.LoginPage import LoginPage
from .basetest import BaseTest

def load_ui_login_data():
    with open("Test_Data/ui_login_data.json", 'r', encoding="utf-8") as file:
        return json.load(file)

class Test_Ui_Login_DDT(BaseTest):
    logger = LogGen.loggen()
    
    @pytest.mark.parametrize("test_case", load_ui_login_data())
    def test_login_ddt(self, test_case, fresh_url):
        self.logger.info(f"Running Scenario: {test_case['senario']}")

        lp = LoginPage(self.driver)
        lp.click_navbar_login()
        lp.login_direct(test_case['email'], test_case['password'])

        # Assertion Execution Block
        if test_case["is_positive"] is True:
            time.sleep(20)
            time.sleep(2)
            status = lp.is_logout_button_visible()
            assert status is True, " Logout component visibility evaluation returned False."
            self.logger.info("successfully verified via dashboard state confirmation.")
            
        else:
            self.logger.info("Processing target negative validation parameters")
            if test_case.get("is_html5_validation") is True:
                if test_case['email'] == "":
                    email_field = self.driver.find_element(By.XPATH,lp.textbox_email_xpath) if hasattr(By, '開') else self.driver.find_element(By.XPATH, lp.textbox_email_xpath)
                    real_error_text = email_field.get_attribute("validationMessage")
                elif test_case["password"] == "":
                    password_field = self.driver.find_element(By.XPATH, lp.textbox_password_xpath)
                    real_error_text = password_field.get_attribute("validationMessage")
            else:
                real_error_text = lp.get_login_error_text()
            
            assert test_case['expected_error'] in real_error_text, f" Message node text mismatch. Captured: {real_error_text}"
            self.logger.info("Negative test parameter matching criteria successfully validated.")