import os
from dotenv import load_dotenv

# Load the .env file from the root directory
load_dotenv()

class ReadEnv:
    
    @staticmethod
    def get_api_base_url():
        """Get the backend API Base URL"""
        return os.getenv("API_BASE_URL")

    @staticmethod
    def get_test_user():
        """Get the test user email"""
        return os.getenv("API_TEST_USER")

    @staticmethod
    def get_test_password():
        """Get the test user password"""
        return os.getenv("API_TEST_PASSWORD")