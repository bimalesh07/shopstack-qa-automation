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
        self.logger.info(f"Scenario: {test_case['senario']}")

        lp = LoginPage(self.driver)
        lp.click_navbar_login()
        lp.login_direct(test_case['email'], test_case['password'])

        if test_case["is_positive"] is True:
            time.sleep(22)
            status = lp.is_logout_button_visible()
            assert status is True, "Login session failed for positive case."
            self.logger.info("Positive login verified successfully.")
            
        else:
            if test_case.get("is_html5_validation") is True:
                if test_case['email'] == "":
                    field = self.driver.find_element(By.XPATH, lp.textbox_email_xpath)
                elif test_case["password"] == "":
                    field = self.driver.find_element(By.XPATH, lp.textbox_password_xpath)
                real_error_text = field.get_attribute("validationMessage")
            else:
                real_error_text = lp.get_login_error_text()
            
            assert test_case['expected_error'] in real_error_text, f"Unexpected error message: {real_error_text}"
            self.logger.info("Negative login error verified successfully.")