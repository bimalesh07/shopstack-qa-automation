import os
import time
import pytest
from .basetest import BaseTest
from PageObjects.LoginPage import LoginPage
from Utilities.customLogger import LogGen

class Test_002_Direct_Login(BaseTest):
    logger = LogGen.loggen()
    
    user_email = os.getenv("LOGIN_USERNAME") or "bimaleshy49@gmail.com"
    user_password = os.getenv("LOGIN_PASSWORD") or "Password@123"

    def test_01_direct_login_invalid(self, fresh_url):
        """Verify that system blocks unauthorized access when using an incorrect password."""
        self.logger.info("Executing test case: Direct Login Invalid Credentials")
        lp = LoginPage(self.driver)

        lp.click_navbar_login()
        
        self.logger.info("Submitting valid email with an incorrect password")
        lp.login_direct(self.user_email, "wrong@pass123")

        error_box_text = lp.get_login_error_text().lower()
        self.logger.info(f"Captured UI error message: {error_box_text}")

        assert "invalid" in error_box_text or "credentials" in error_box_text or "wrong" in error_box_text, f"Validation check failed: {error_box_text}"
        assert lp.is_logout_button_visible() is False
        self.logger.info("Test passed: System successfully blocked unauthorized access.")
    
    @pytest.mark.skip(reason="Skipping manual OTP input in Jenkins pipeline")
    def test_02_direct_login_valid(self, fresh_url):
        """Verify successful user authentication with valid credentials and manual OTP verification."""
        self.logger.info("Executing test case: Direct Login Positive Flow")
        lp = LoginPage(self.driver)
        
        lp.click_navbar_login()

        self.logger.info(f"Attempting authorization for user: {self.user_email}")
        lp.login_direct(self.user_email, self.user_password)

        self.logger.info("Pausing execution for manual OTP entry on the browser screen...")
        time.sleep(25)
        time.sleep(2) 
        
        status = lp.is_logout_button_visible()
        assert status is True, "Login validation failed: Logout component not located."
        self.logger.info("Test passed: Direct login validation with OTP confirmed.")