import pytest
import requests
from Utilities.customLogger import LogGen
from API_Endpoints.AuthEndPoints import AuthEndpoints
import time

class Test_ShopStack_Auth_Negative_Endpoints:
    logger = LogGen.loggen()

    real_base_email = "bimaleshy49"
    neg_test_email = f"{real_base_email}+ne{int(time.time())}@gmail.com"
    test_user_password = "SecurePassword123"

    def test_neg_01_duplicate_email_registration_erro(self, auth_client):
        self.logger.info("Starting test: Duplicate registration check")

        payload = {
            "email": self.neg_test_email,
            "name": "Bimalesh test",
            "phone": "888888888",
            "password": self.test_user_password,
            "password2": self.test_user_password
        }
        first_res = auth_client.Signup(payload, role="customers")
        assert first_res.status_code in [200, 201]
        self.logger.info("First signup completed. Now trying duplicate registration.")

        duplicate_res = auth_client.Signup(payload, role="customers")
        assert duplicate_res.status_code in [400, 409]
        self.logger.info(f"Duplicate signup rejected with status: {duplicate_res.status_code}")

    def test_neg_02_login_with_wrong_password_error(self, auth_client):
        self.logger.info("Starting test: Login with wrong password")

        respone = auth_client.login(self.neg_test_email, "wronpassword@999")
        assert respone.status_code in [400, 401]
        self.logger.info(f"Wrong password login rejected with status: {respone.status_code}")

    def test_neg_03_login_with_invalid_email_error(self, auth_client):
        self.logger.info("Starting test: Login with fake email")
        
        response = auth_client.login("biamlesh2@gmail.com", self.test_user_password)  
        assert response.status_code in [400, 401, 404]
        self.logger.info(f"Fake email login rejected with status: {response.status_code}")