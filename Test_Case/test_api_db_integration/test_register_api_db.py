import pytest
from Utilities.db_helper import DbHelper

class Test_Register_User_And_Verify_In_Database:
    
    def test_register_user_and_verify_in_database(self, auth_client, db_session):
        """Verify successful user lifecycle entry via API signup and cross-validate record state inside the database layer."""
        test_email = "bimaleshky@gmail.com"
        
        payload = {
            "email": test_email,
            "name": "yadavbimalesh",
            "phone": "555777787",
            "password1": "1234567bky",
            "password2": "1234567bky"
        }
        
        #  API Endpoint Target Invocation
        response = auth_client.Signup(payload, role="customers")
        assert response.status_code == 201, f"Validation check failed: Registration request rejected with status code {response.status_code}"
        
        #Database Persistence Layer Cross-Verification
        sql_query = f"SELECT name FROM users_user WHERE email = '{test_email}';"
        
        # Access database execution framework utilizing the active db_session context
        db_result = DbHelper.execute_select(db_session, sql_query) 

        #Structural Integrity Validation
        assert db_result is not None, "Validation check failed: Targeted user record not located inside the database query response."
        assert db_result[0] == "yadavbimalesh", f"Validation check failed: Name property property mismatch. Captured: {db_result[0]}"