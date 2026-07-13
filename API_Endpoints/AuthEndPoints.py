import requests
from Utilities.customLogger import LogGen

class AuthEndpoints:
    # Connecting to your fresh, dedicated API logger
    logger = LogGen.apiloggen()
    
    def __init__(self, base_url):
        self.base_url = base_url
    
    def Signup(self, user_data, role = 'customers'):
        """Signup: Customers and Vendor both so we Dynamic endpoints handles"""
        if role.lower() == 'vendor':
            url = f"{self.base_url}/vendor/register/"  # Added trailing slash
        else:
            url = f"{self.base_url}/register/"
            
        self.logger.info(f"--- Creating a new {role} account ---")
        self.logger.info(f"Sending registration details to: {url}")
        self.logger.info(f"User data being submitted: {user_data}")
        
        response = requests.post(url, json=user_data)
        
        self.logger.info(f"Server responded with status code: {response.status_code}")
        self.logger.info(f"Server response details: {response.text}")
        return response            
    
    def verify_opt(self, email, otp):
        """Verify otp Registration Login after verify the otp"""
        url = f"{self.base_url}/verify-otp/"  # Added trailing slash '/'
        payload = {"email": email, "otp": otp}
        
        self.logger.info(f"--- Verifying OTP for {email} ---")
        self.logger.info(f"Submitting OTP code [{otp}] to: {url}")
        
        response = requests.post(url, json=payload)
        
        self.logger.info(f"Verification status code: {response.status_code}")
        self.logger.info(f"Verification response details: {response.text}")
        return response
    
    def resend_otp(self, email):
        """RESEND OTP: If Otp not come then we target resend otp"""
        url = f"{self.base_url}/resend-otp/"  # Added trailing slash '/'
        payload = {"email": email}
        
        self.logger.info(f"--- Requesting a new OTP link/code ---")
        self.logger.info(f"Asking server to resend code to: {url}")
        
        response = requests.post(url, json=payload)
        
        self.logger.info(f"Resend request finished with status: {response.status_code}")
        self.logger.info(f"Resend response details: {response.text}")
        return response
    
    def login(self, email, password):
        url = f"{self.base_url}/login/"  
        payload = {"email": email, "password": password}
        
        self.logger.info(f"--- Attempting secure login ---")
        self.logger.info(f"Trying to login user: {email} at {url}")
        
        response = requests.post(url, json=payload)
        
        self.logger.info(f"Login attempt returned status: {response.status_code}")
        self.logger.info(f"Login response details: {response.text}")
        return response
    
    def get_profile(self, token):
        """Get Profile"""
        url = f"{self.base_url}/profile/"
        headers = {"Authorization": f"Bearer {token}"}
        
        self.logger.info(f"--- Fetching user account profile ---")
        self.logger.info(f"Requesting secure profile data from: {url}")
        
        response = requests.get(url, headers=headers)
        
        self.logger.info(f"Profile fetch returned status: {response.status_code}")
        return response
    
    def logout(self, refresh_token, access_token=None):
        url = f"{self.base_url}/logout/"
        payload = {"refresh": refresh_token}
        
        # If access token is passed, create headers
        headers = {}
        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"
        
        self.logger.info(f"--- Terminating user session (Logout) ---")
        self.logger.info(f"Sending logout request to clean session at: {url}")
        
        # Include headers in the request
        response = requests.post(url, json=payload, headers=headers)
        
        self.logger.info(f"Logout finished with status: {response.status_code}")
        return response