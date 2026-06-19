import pytest
from Utilities.db_helper import DbHelper

class Test_Register_user_and_verify_in_database:
    
    def test_register_user_and_verify_in_database(self, auth_client, db_session):
        test_email = "bimaleshky@gmail.com"
        
        # Fix: replaced '=' with ':' in dictionary
        payload = {
            "email": test_email,
            "name": "yadavbimalesh",
            "phone": "555777787",
            "password1": "1234567bky",
            "password2": "1234567bky"
        }
        
        # 1. Call API to sign up
        response = auth_client.Signup(payload, role="customers")
        
        # Verify if user registered successfully
        assert response.status_code == 201, f"❌ Registration failed! Status code: {response.status_code}"
        print("✅ Step 1: User Registered via API successfully!")

        # --------------------------------------------------------------------
        # VERIFY THE DB TESTING
        # --------------------------------------------------------------------
        # Table is users_user
        sql_query = f"SELECT name FROM users_user WHERE email = '{test_email}';"
        
        # Use DbHelper select method
        db_result = DbHelper.execute_select(self.db, sql_query) 

        # Final Checking (Assertions)
        assert db_result is not None, "❌ Fail: User not found in database!"
        
        # If db_result is a tuple, check the first element
        assert db_result[0] == "yadavbimalesh", f"❌ Fail: Incorrect name in DB! Found: {db_result[0]}"
        
        print("✅ Step 2: Database verified successfully! Data is absolute perfect.")