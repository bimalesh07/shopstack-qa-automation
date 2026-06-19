import pytest
from Utilities.db_helper import DbHelper

class Test_Register_user_and_verify_in_database:
    
    def test_register_user_and_verify_in_database(self, auth_client, db_session):
        test_email = "bimaleshky@gmail.com"
        
        # ❌ FIX: '=' ki jagah ':' lagaya dictionary ke andar
        payload = {
            "email": test_email,
            "name": "yadavbimalesh",
            "phone": "555777787",
            "password1": "1234567bky",
            "password2": "1234567bky"
        }
        
        # 1. API Hit ki signup karne ke liye
        response = auth_client.Signup(payload, role="customers")
        
        # Verify kiya ki user register hua ya nahi
        assert response.status_code == 201, f"❌ Registration failed! Status code: {response.status_code}"
        print("✅ Step 1: User Registered via API successfully!")

        # --------------------------------------------------------------------
        # 🗄️ VERIFY THE DB TESTING (Completing the code)
        # --------------------------------------------------------------------
        # Tumhaari table users_user hai toh query wahi rakhi
        sql_query = f"SELECT name FROM users_user WHERE email = '{test_email}';"
        
        # Tumhaare DBHelper ka select method use kiya
        db_result = DbHelper.execute_select(self.db, sql_query) 

        # Final Checking (Assertions)
        assert db_result is not None, "❌ Fail: User database mein nahi mila!"
        
        # db_result agar tuple form mein data deta hai toh tuple ka pehla element check karo
        assert db_result[0] == "yadavbimalesh", f"❌ Fail: DB mein naam galat hai! Mila: {db_result[0]}"
        
        print("✅ Step 2: Database verified successfully! Data is absolute perfect.")