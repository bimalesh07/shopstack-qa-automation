import pytest
import requests
from Utilities.customLogger import LogGen
from API_Endpoints.AuthEndPoints import AuthEndpoints
import time

class Test_ShopStack_Auth_Negative_Endpoints:
    logger = LogGen.loggen()

    #negative testing
    real_base_email = "bimaleshy49"
    neg_test_email = f"{real_base_email}+ne{int(time.time())}@gmail.com"
    test_user_password = "SecurePassword123"
    

    #negative Test: Duplicate Email Registration
    def  test_neg_01_duplicate_email_registration_erro(self, auth_client):
        self.logger.info("Testing Duplicate Registration")

        payload ={
            "email": self.neg_test_email,
            "name":"Bimalesh test",
            "phone":"888888888",
            "password": self.test_user_password,
            "password2": self.test_user_password
        }
        first_res = auth_client.Signup(payload, role="customers")
        assert first_res.status_code in [200, 201]
        self.logger.info("first registatin setu[ competed trying duplicate Now]")

        #duplicate register 
        duplicate_res = auth_client.Signup(payload, role="customers")
        assert duplicate_res.status_code in [400, 409]
        self.logger.info(f"Passed Server sucessfully rejected duplicate regisration with status:{duplicate_res.status_code}")

    """Negative TEST: Login with Wrong Password"""
    def test_neg_02_login_with_wrong_password_error(self, auth_client):
        """Negative: Try to login with a known email but a wrong password"""
        self.logger.info("Testing login with Wrong Password")

        respone = auth_client.login(self.neg_test_email, "wronpassword@999")
        """if server rejected then staus code 400 ya 401"""
        assert respone.status_code in [400, 401]
        self.logger.info("f[PASSED] server successfully rejected wrong password with staus code:{response.status_code}")

    """Login with NON Existent Email"""
    def test_neg_03_login_with_invalid_email_error(self, auth_client):
        self.logger.info("Testing Login with fake Email ")
        response = auth_client.login("biamlesh2@gmail.com", self.test_user_password)  
        assert response.status_code in [400, 401, 404]
        self.logger.info(f"[PASSED] Server Successfully rejected fake email Login with stauscode:{response.status_code}")
