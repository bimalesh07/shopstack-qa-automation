# Test_Case/test_api/conftest.py

import pytest
import time
from Utilities.readEnv import ReadEnv
from API_Endpoints.AuthEndPoints import AuthEndpoints
from API_Endpoints.ProductEndpoints import ProductEndpoints
from API_Endpoints.ProductEndpoints import ProductEndpoints
from Utilities.customLogger import LogGen

# Connecting to your dedicated fresh API logger file (automation_api.log)
logger = LogGen.apiloggen()

# Global variables so that the same user is used in the entire run and data is not mixed
FIXED_TEST_EMAIL = f"shopstack_live_{int(time.time())}@test.com"
FIXED_PASSWORD = "SecurePassword123"
IS_REGISTERED = False  # Flag to check if user creation is already done


# =========================================================================
# FIXTURE 1: Master Remote Control
# =========================================================================
@pytest.fixture(scope="class")
def auth_client():
    """
    🎛️ Setting up the core API client.
    Using this client, you can run Signup, login, verify_otp, and get_profile.
    """
    logger.info("--- [SETUP] Initializing the Master API Client ---")
    base_url = ReadEnv.get_api_base_url()
    logger.info(f"Successfully connected to the live environment at: {base_url}")
    return AuthEndpoints(base_url)

@pytest.fixture(scope="class")
def product_client():
    logger.info("Initializing product")
    base_url = ReadEnv.get_api_base_url()
    return ProductEndpoints(base_url)


# =========================================================================
# FIXTURE 2: Token engine to provide token for Cart/Profile
# =========================================================================
@pytest.fixture(scope="class")
def user_token(auth_client):
    """
    🔑 Smart Token Autopilot:
    - First time: Directly registers the user and grabs the instant login token.
    - Next times (If logged out): Bypasses registration, hits Login, and asks 
      you for the real email OTP in the terminal to fetch a fresh token!
    """
    global IS_REGISTERED, FIXED_TEST_EMAIL, FIXED_PASSWORD
    
    logger.info("--- [AUTOPILOT] Token verification engine requested ---")
    
    # ROUTE A: New user -> Direct register (login token is in registration response)
    # -------------------------------------------------------------------------
    if not IS_REGISTERED:
        logger.info(f"Creating a fresh permanent user for this test run: {FIXED_TEST_EMAIL}")
        
        signup_payload = {
            "email": FIXED_TEST_EMAIL,
            "name": "ShopStack Real Tester",
            "phone": "9999999999",
            "password": FIXED_PASSWORD,
            "password2": FIXED_PASSWORD
        }
        
        # Hitting signup API
        reg_response = auth_client.Signup(signup_payload, role='customers')
        
        if reg_response.status_code == 201 or reg_response.status_code == 200:
            IS_REGISTERED = True  # Set flag to True so registration is not repeated
            
            # Register response contains the login token directly
            access_token = reg_response.json().get("access_token")
            logger.info("🟢 User successfully created! Extracted direct login token from registration response.")
            return access_token
        else:
            logger.error(f"Failed to create the background user: {reg_response.text}")
            raise Exception("❌ Background Initial Registration Failed!")

    # ROUTE B: User already registered or logged out -> Login + OTP Flow
    # -------------------------------------------------------------------------
    else:
        logger.info(f"User already exists in DB. Skipping registration, hitting Login for: {FIXED_TEST_EMAIL}")
        
        # Hitting login API -> This triggers the real email OTP from your backend via Redis
        login_response = auth_client.login(FIXED_TEST_EMAIL, FIXED_PASSWORD)
        logger.info("Login credentials sent. Server is dispatching a real OTP to your email inbox...")
        
        # Stopping script to accept manual input from the tester via terminal
        print(f"\n📨 [SECURITY ALERT] A real login OTP has been sent to your email: {FIXED_TEST_EMAIL}")
        print("👉 Please check your mailbox/spam folder, grab the code, and enter it below.")
        
        logger.info("Execution paused. Waiting for the tester to type the login OTP in terminal...")
        real_otp = input("⌨️  ENTER THE LOGIN OTP FROM YOUR EMAIL AND PRESS ENTER: ")
        
        logger.info(f"Resuming workflow. Submitting entered OTP [{real_otp}] to fetch the session token...")
        
        # Submitting the manually typed OTP to verify and activate the login session
        otp_response = auth_client.verify_opt(FIXED_TEST_EMAIL, real_otp)
        
        if otp_response.status_code != 200:
            logger.error("Login verification failed due to incorrect OTP entry!")
            raise Exception(f"❌ Login Failed! Incorrect OTP typed in terminal: {otp_response.text}")
            
        # Extracting the fresh new token after login verification
        access_token = otp_response.json().get("access_token")
        logger.info("Successfully fetched the new active token after secure login verification.")
        return access_token