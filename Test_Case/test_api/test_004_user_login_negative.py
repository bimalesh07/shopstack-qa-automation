import pytest
from Utilities.customLogger import LogGen

class Test_User_Login_API_Negative:
    logger = LogGen.apiloggen()
    
    from Test_Case.test_api.conftest import FIXED_TEST_EMAIL
    ghost_email = "non_existent_bhai_999@ghost.com"
    wrong_password = "InvalidPassword@999"

    def test_neg_login_01_wrong_password(self, auth_client):
        self.logger.info("Step 1: Login with invalid password")
        
        response = auth_client.login(self.FIXED_TEST_EMAIL, self.wrong_password)
        
        assert response.status_code in [400, 401]
        res_text = response.text.lower()
        assert "invalid" in res_text or "credentials" in res_text or "unauthorized" in res_text
        self.logger.info("Wrong password successfully blocked.")

    def test_neg_login_02_ghost_user(self, auth_client):
        self.logger.info("Step 2: Login with unregistered email")
        
        response = auth_client.login(self.ghost_email, "AnyPassword123")
        assert response.status_code in [400, 401, 404]
        self.logger.info("Unregistered user request rejected cleanly.")

    def test_neg_login_03_invalid_login_otp(self, auth_client):
        self.logger.info("Step 3: Submitting corrupted OTP token")
        
        corrupted_otp = "999999"
        response = auth_client.verify_opt(self.FIXED_TEST_EMAIL, corrupted_otp)
        
        assert response.status_code == 400
        res_text = response.text.lower()
        assert "invalid" in res_text or "expired" in res_text or "wrong" in res_text
        self.logger.info("Invalid OTP submission successfully blocked.")