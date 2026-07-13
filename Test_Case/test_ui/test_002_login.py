import os
import time
import pytest
from Test_Case.test_ui.basetest import BaseTest
from PageObjects.LoginPage import LoginPage
from Utilities.customLogger import LogGen

class Test_002_Direct_Login(BaseTest):
    logger = LogGen.loggen()
    
    user_email = os.getenv("LOGIN_USERNAME") or "bimaleshy49@gmail.com"
    user_password = os.getenv("LOGIN_PASSWORD") or "Password@123"

    def test_01_direct_login_invalid(self, fresh_url):
        self.logger.info("Running invalid login test...")
        lp = LoginPage(self.driver)
        lp.click_navbar_login()
        lp.login_direct(self.user_email, "wrong@pass123")
        
        error_box_text = lp.get_login_error_text().lower()
        self.logger.info(f"UI Error message: {error_box_text}")
        
        assert "invalid" in error_box_text or "credentials" in error_box_text or "wrong" in error_box_text, f"Validation check failed: {error_box_text}"
        assert lp.is_logout_button_visible() is False

    @pytest.mark.skip(reason="Skipping manual OTP input in Jenkins pipeline")
    def test_02_direct_login_valid(self, fresh_url):
        self.logger.info("Running valid login test...")
        lp = LoginPage(self.driver)
        lp.click_navbar_login()
        lp.login_direct(self.user_email, self.user_password)
        
        time.sleep(25)
        
        status = lp.is_logout_button_visible()
        assert status is True, "Login validation failed: Logout component not located."