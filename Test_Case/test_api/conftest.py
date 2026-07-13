import pytest
import time
from Utilities.readEnv import ReadEnv
from API_Endpoints.AuthEndPoints import AuthEndpoints
from API_Endpoints.ProductEndpoints import ProductEndpoints
from Utilities.customLogger import LogGen

logger = LogGen.apiloggen()

FIXED_TEST_EMAIL = f"shopstack_live_{int(time.time())}@test.com"
FIXED_PASSWORD = "SecurePassword123"
IS_REGISTERED = False 

@pytest.fixture(scope="class")
def auth_client():
    logger.info("Starting Auth API client connection setup.")
    base_url = ReadEnv.get_api_base_url()
    logger.info(f"Successfully connected to Auth endpoint: {base_url}")
    return AuthEndpoints(base_url)

@pytest.fixture(scope="class")
def product_client():
    logger.info("Starting Product API client connection setup.")
    base_url = ReadEnv.get_api_base_url()
    return ProductEndpoints(base_url)



@pytest.fixture(scope="class")
def user_token(auth_client):
    global IS_REGISTERED, FIXED_TEST_EMAIL, FIXED_PASSWORD
    
    logger.info("Token request received by the automation engine.")
    
    #Register user and get token directly from response
    if not IS_REGISTERED:
        logger.info(f"Creating a brand new test user for this execution: {FIXED_TEST_EMAIL}")
        
        signup_payload = {
            "email": FIXED_TEST_EMAIL,
            "name": "ShopStack Real Tester",
            "phone": "9999999999",
            "password": FIXED_PASSWORD,
            "password2": FIXED_PASSWORD
        }
        
        reg_response = auth_client.Signup(signup_payload, role='customers')
        
        if reg_response.status_code in [200, 201]:
            IS_REGISTERED = True
            access_token = reg_response.json().get("access_token")
            logger.info("User registered successfully. Token extracted from signup response.")
            return access_token
        else:
            logger.error(f"Error: Initial background registration failed: {reg_response.text}")
            raise Exception("Background user registration failed.")

    #  User already exist Perform login and ask for OTP in terminal
    else:
        logger.info(f"User already exists in system. Skipping signup and hitting login for: {FIXED_TEST_EMAIL}")
        
        login_response = auth_client.login(FIXED_TEST_EMAIL, FIXED_PASSWORD)
        logger.info("Login request sent. Server is sending a live OTP to your email box.")
        
        logger.info("Waiting for tester to enter login OTP in the terminal.")
        real_otp = input("Please type the live login OTP from your email and press Enter: ")
        
        logger.info("Resuming test run. Submitting entered OTP token to verification endpoint.")
        otp_response = auth_client.verify_opt(FIXED_TEST_EMAIL, real_otp)
        
        if otp_response.status_code != 200:
            logger.error("Verification failed: Incorrect login OTP code entered.")
            raise Exception(f"Login failed due to incorrect OTP text: {otp_response.text}")
            
        access_token = otp_response.json().get("access_token")
        logger.info("OTP verification passed. Active session token updated successfully.")
        return access_token