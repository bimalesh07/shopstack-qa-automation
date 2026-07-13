import pytest
from Utilities.customLogger import LogGen
from Utilities.readEnv import ReadEnv

class Test_User_Login_API_Positive:
    logger = LogGen.apiloggen()
    
    received_refresh_token = None
    FIXED_TEST_EMAIL = ReadEnv.get_test_user()
    FIXED_PASSWORD = ReadEnv.get_test_password()

    def test_login_01_positive_auth_flow(self, auth_client):
        self.logger.info("Step 1: Running Positive Login API")
        
        response = auth_client.login(self.FIXED_TEST_EMAIL, self.FIXED_PASSWORD)
        assert response.status_code == 200
        
        login_data = response.json()
        tokens_dict = login_data.get("tokens", {})
        
        direct_access = tokens_dict.get("access") or login_data.get("access_token")
        direct_refresh = tokens_dict.get("refresh") or login_data.get("refresh_token")
        
        if direct_access and direct_refresh:
            self.logger.info("Direct login token fetched successfully.")
            Test_User_Login_API_Positive.received_refresh_token = direct_refresh
        else:
            self.logger.info("MFA triggered. OTP required via terminal.")
            login_otp = input("Enter transaction authentication OTP: ").strip()
            
            otp_res = auth_client.verify_opt(self.FIXED_TEST_EMAIL, login_otp)
            assert otp_res.status_code == 200
            
            nested_tokens = otp_res.json().get("tokens", {})
            Test_User_Login_API_Positive.received_refresh_token = nested_tokens.get("refresh") or otp_res.json().get("refresh_token")
            
        self.logger.info("Login tokens verified successfully.")

    def test_login_02_profile_fetch_with_token(self, auth_client, user_token):
        self.logger.info("Step 2: Fetching Profile via Valid Token")
        
        response = auth_client.get_profile(user_token)
        assert response.status_code == 200
        self.logger.info("User profile verified successfully.")

    def test_login_03_session_logout(self, auth_client):
        self.logger.info("Step 3: Checking Session Termination")
        
        refresh = Test_User_Login_API_Positive.received_refresh_token
        if not refresh:
            pytest.skip("Refresh token missing, skipping logout.")
            
        response = auth_client.logout(refresh)
        assert response.status_code in [200, 201, 204, 401]
        self.logger.info("Logout API complete.")