import pytest
import time
import json
from selenium.webdriver.common.by import By
from Utilities.customLogger import LogGen
from PageObjects.LoginPage import LoginPage
from .basetest import BaseTest

def load_ui_login_data():
    """test_data folders as complete login json load data """
    with open("Test_Data/ui_login_data.json", 'r' , encoding="utf-8") as file:
        return json.load(file)
    

class Test_Ui_Login_DDT(BaseTest):
    logger = LogGen.loggen()
    @pytest.mark.parametrize("test_case", load_ui_login_data())
    def test_login_ddt(self, test_case):
        self.logger.info("Runing  Senario: {test_case['senario']}")

        lp = LoginPage(self.driver)
        lp.click_navbar_login()
        lp.login_direct(test_case['email'], test_case['password'])

        """Asserton """
        if test_case["is_positive"] is True:
            time.sleep(20)
            time.sleep(2)
            status = lp.is_logout_button_visible()
            assert status is True, "❌ Failed Login Flow: Logout button function returned False!"
            self.logger.info("🎉 SUCCESS: Valid login validated completely with avatar dropdown check!")
            
        else:
            self.logger.info("Checking  neagative validation outcome")
            if test_case.get("is_html5_validation") is True:
                if test_case['email'] =="":
                 email_field = self.driver.find_element(By.XPATH, lp.textbox_email_xpath)
                 real_error_text = email_field.get_attribute("validationMessage")

                elif test_case["password"] =="":
                    password_feild = self.driver.find_element(By.XPATH, lp.textbox_password_xpath)
                    real_error_text = password_feild.get_attribute("validationMessage")
            else:
                real_error_text = lp.get_login_error_text()
            
            assert test_case['expected_error'] in real_error_text, " Failed : MESAGE MISMATCH"
                
            