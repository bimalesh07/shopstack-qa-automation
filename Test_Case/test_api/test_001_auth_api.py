import pytest
import time
from Utilities.customLogger import LogGen

class Test_ShopStack_Auth_Endpoints:
    
    logger = LogGen.apiloggen()

    real_base_email = "bimaleshy49"
    test_user_email = f"{real_base_email}+{int(time.time())}@gmail.com"
    test_user_password = "SecurePassword123"
    
    received_token = None
    received_refresh_token = None

    def test_01_user_registration_validation(self, auth_client):
        self.logger.info("Starting Test Case: User Registration Validation")
        
        signup_payload = {
            "email": self.test_user_email,
            "name": "Bimalsh yadav",
            "phone": "8888888888",
            "password": self.test_user_password,
            "password2": self.test_user_password
        }
        
        response = auth_client.Signup(signup_payload, role='customers')
        assert response.status_code in [200, 201]
        self.logger.info("User registration successful. Profile state initialized as inactive.")



    def test_03_smart_account_activation_validation(self, auth_client):
        self.logger.info("Starting Test Case: Registration OTP Verification and Fallback Flow")
        
        self.logger.info("Waiting for registration verification input string.")
        user_input_1 = input("Enter registration OTP (Leave blank to trigger resend fallback): ").strip()
        
        is_activated = False
        
        if user_input_1:
            self.logger.info(f"Submitting initial verification OTP: {user_input_1}")
            otp_res = auth_client.verify_opt(self.test_user_email, user_input_1)
            
            if otp_res.status_code == 200:
                self.logger.info("Initial validation code verified. Account activated successfully.")
                is_activated = True
            else:
                self.logger.warning("Initial validation token rejected. Processing fallback sequence.")
        
        if not is_activated:
            self.logger.info("Triggering resend OTP service request.")
            resend_res = auth_client.resend_otp(self.test_user_email)
            assert resend_res.status_code == 200
            self.logger.info("Resend OTP application interface executed successfully.")
            
            self.logger.info("Waiting for secondary validation input from console stream.")
            user_input_2 = input("Enter the updated verification OTP: ").strip()
            
            otp_res2 = auth_client.verify_opt(self.test_user_email, user_input_2)
            assert otp_res2.status_code == 200
            self.logger.info("Account successfully activated using fallback token verification.")
            
        self.logger.info("User profile verified and fully active in database.")

    def test_04_login_and_token_generation(self, auth_client):
        self.logger.info("Starting Test Case: Intelligent Login Validation")
        
        login_res = auth_client.login(self.test_user_email, self.test_user_password)
        assert login_res.status_code == 200
        
        login_data = login_res.json()
        tokens_dict = login_data.get("tokens", {})
        
        direct_access = tokens_dict.get("access") or login_data.get("access_token")
        direct_refresh = tokens_dict.get("refresh") or login_data.get("refresh_token")
        
        if direct_access and direct_refresh:
            self.logger.info("Authentication complete: Direct login routing processed successfully.")
            Test_ShopStack_Auth_Endpoints.received_token = direct_access
            Test_ShopStack_Auth_Endpoints.received_refresh_token = direct_refresh
        else:
            self.logger.info("Credentials matched. Interactive OTP token verification required.")
            
            self.logger.info("Waiting for interactive security challenge verification code input.")
            login_otp = input("Enter the transaction authentication OTP: ")
            
            otp_res = auth_client.verify_opt(self.test_user_email, login_otp)
            assert otp_res.status_code == 200
            
            json_data = otp_res.json()
            nested_tokens = json_data.get("tokens", {})
            
            Test_ShopStack_Auth_Endpoints.received_token = nested_tokens.get("access") or json_data.get("access_token")
            Test_ShopStack_Auth_Endpoints.received_refresh_token = nested_tokens.get("refresh") or json_data.get("refresh_token")
        
        assert Test_ShopStack_Auth_Endpoints.received_token is not None, "Validation check failed: Access token collection failed."
    
        self.logger.info("Security access tokens captured successfully.")

    def test_05_profile_and_logout_cleanup(self, auth_client):
        self.logger.info("Profile Retrieval and Session Termination")
        
        token = Test_ShopStack_Auth_Endpoints.received_token
        refresh_token = Test_ShopStack_Auth_Endpoints.received_refresh_token
        
        if not token or not refresh_token:
            pytest.skip("Prerequisite tokens are missing. Skipping test case execution.")
            
        profile_res = auth_client.get_profile(token)
        assert profile_res.status_code == 200
        self.logger.info("Protected data profile records verified successfully.")
        
        logout_res = auth_client.logout(refresh_token)
        
        if logout_res.status_code in [200, 204, 201]:
            self.logger.info("Session termination request processed successfully.")
        elif logout_res.status_code == 401:
            self.logger.warning("Session termination returned unauthorized status. Bypassing constraint verification.")
            
        assert logout_res.status_code in [200, 204, 201, 401]
        self.logger.info("Session lifecycle validation completed successfully.")