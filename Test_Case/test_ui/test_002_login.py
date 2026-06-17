
import os
import time
from Test_Case.basetest import BaseTest
from PageObjects.LoginPage import LoginPage
from Utilities.customLogger import LogGen
import pytest

class Test_002_Direct_Login(BaseTest):
    logger = LogGen.loggen()
    
    # Robust Fallback Matrix: Agar environment None de, toh static string utha lo
    user_email = os.getenv("LOGIN_USERNAME") if os.getenv("LOGIN_USERNAME") else "bimaleshy49@gmail.com"
    user_password = os.getenv("LOGIN_PASSWORD") if os.getenv("LOGIN_PASSWORD") else "Password@123"

    def test_01_direct_login_invlaid(self):
        self.logger.info("*************** STARTING INVALID LOGIN TEST ***************")
        lp = LoginPage(self.driver)

        lp.click_navbar_login()
         
        self.logger.info("Sending valid email with an incorrect password")
        lp.login_direct(self.user_email, "wrong@pass123")

        error_box_text = lp.get_login_error_text().lower()
        self.logger.info(f"Caught Error Box Text: {error_box_text}")

        assert "invalid" in error_box_text or "credentials" in error_box_text or "wrong" in error_box_text, f"not match box text"

        # Parde ke peeche logic: False == False -> Success!
        assert lp.is_logout_button_visible() == False
        self.logger.info("🎉 PASSED: SYSTEM SUCCESSFULLY blocked the unauthorized access.")
    
    @pytest.mark.skip(reason="Skipping manual OTP input in Jenkins")
    def test_02_direct_login_valid(self):
        self.logger.info("*************** STARTING VALID OTP LOGIN TEST ***************")
        lp = LoginPage(self.driver)
        
        lp.click_navbar_login()

        self.logger.info(f"Attempting authorization for user: {self.user_email}")
        lp.login_direct(self.user_email, self.user_password)

        self.logger.info("⏳ MANUAL ACTION: Enter a OTP right now and click verify button...")
        time.sleep(25) # Shanti se 25 second ke andar enter dabao bhai
        
        time.sleep(2) # Landing stabilization
        
        status = lp.is_logout_button_visible()
        assert status == True, "❌ Login Flow Failed: Logout dropdown flow element not located!"
        self.logger.info("🎉 SUCCESS: Direct login validation with OTP Confirmed!")