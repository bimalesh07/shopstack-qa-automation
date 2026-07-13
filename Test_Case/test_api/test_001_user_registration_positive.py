import pytest
import time
from Utilities.customLogger import LogGen
from Utilities.readEnv import ReadEnv

class Test_User_Registration_API_Positive:
    logger = LogGen.apiloggen()
    
    #unique_suffix = int(time.time())
    #customer_email = f"api_cust_{unique_suffix}@gmail.com"
    #vendor_email = f"api_vend_{unique_suffix}@gmail.com"
    customer_email = ReadEnv.get_test_user()
    password=ReadEnv.get_test_password()

    def test_reg_01_customer_positive_workflow(self, auth_client):
        self.logger.info("Running Positive Customer Registration API")
        
        payload = {
            "email": self.customer_email,
            "name": "Kamalesh Yadav",
            "phone": "7050863365",
            "password": self.password,
            "password2": self.password
        }
        
        response = auth_client.Signup(payload, role='customers')
        assert response.status_code in [200, 201]
        
        user_otp = input(f"\nEnter the validation OTP sent to {self.customer_email}: ").strip()
        otp_res = auth_client.verify_opt(self.customer_email, user_otp)
        
        assert otp_res.status_code == 200
        self.logger.info("Customer registration completed successfully.")

    pytest.mark.skip("skip for now")
    def test_reg_02_vendor_positive_workflow(self, auth_client):
        self.logger.info("Running Positive Vendor Registration API")
        
        payload = {
            "email": self.vendor_email,
            "name": "Bhai Store Master",
            "phone": "9123456789",
            "password": self.password,
            "password2": self.password,
            "shop_name": "Digital Hub",
            "description": "Premium automation endpoints tests items vendor."
        }
        
        response = auth_client.Signup(payload, role='vendor')
        assert response.status_code in [200, 201]
        
        user_otp = input(f"\nEnter the validation OTP sent to {self.vendor_email}: ").strip()
        otp_res = auth_client.verify_opt(self.vendor_email, user_otp)
        
        assert otp_res.status_code == 200
        self.logger.info("Vendor registration completed successfully.")