import pytest
import time
from Utilities.readEnv import ReadEnv
from API_Endpoints.AuthEndPoints import AuthEndpoints
from API_Endpoints.ProductEndpoints import ProductEndpoints
from Utilities.customLogger import LogGen
from Utilities.readEnv import ReadEnv

logger = LogGen.apiloggen()

FIXED_TEST_EMAIL = ReadEnv.get_test_user()
FIXED_PASSWORD = ReadEnv.get_test_password()



@pytest.fixture(scope="session")
def api_context():
    logger.info("********Setup Api *********")
    base_url = ReadEnv.get_api_base_url()
    


    


@pytest.fixture(scope="class")
def auth_client():
    logger.info("Connecting to Auth endpoint...")
    base_url = ReadEnv.get_api_base_url()
    return AuthEndpoints(base_url)

@pytest.fixture(scope="class")
def product_client():
    logger.info("Connecting to Product endpoint...")
    base_url = ReadEnv.get_api_base_url()
    return ProductEndpoints(base_url)


@pytest.fixture(scope="class")
def user_token(auth_client):
    logger.info(f"Initiating login sequence for: {FIXED_TEST_EMAIL}")
    
    login_response = auth_client.login(FIXED_TEST_EMAIL, FIXED_PASSWORD)
    logger.info("Login request sent. Server is sending live OTP.")
    
    real_otp = input("\nEnter the live login OTP from email: ").strip()
    
    logger.info("Verifying OTP...")
    otp_response = auth_client.verify_opt(FIXED_TEST_EMAIL, real_otp)
    
    if otp_response.status_code != 200:
        logger.error("Incorrect OTP code entered.")
        raise Exception(f"OTP Verification failed: {otp_response.text}")
        
    access_token = otp_response.json().get("access_token") or otp_response.json().get("tokens", {}).get("access")
    logger.info("OTP verification passed. Token captured successfully.")
    
    return access_token