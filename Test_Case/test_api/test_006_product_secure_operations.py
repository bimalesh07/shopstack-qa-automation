import pytest
from Utilities.customLogger import LogGen

class Test_ShopStack_Product_Secure_Operations:
    logger = LogGen.apiloggen()
    
    # Class execution memory anchors
    created_product_id = None
    stored_access_token = None
    
    from Test_Case.test_api.conftest import FIXED_TEST_EMAIL, FIXED_PASSWORD

    def test_01_vendor_login(self, auth_client):
        self.logger.info("Step 1: Authenticating Vendor Session")
        response = auth_client.login(self.FIXED_TEST_EMAIL, self.FIXED_PASSWORD)
        assert response.status_code == 200
        
        # dynamic extraction check
        tokens = response.json().get("tokens", {})
        access = tokens.get("access") or response.json().get("access_token")
        
        if not access:
            login_otp = input("Enter Vendor Login OTP: ").strip()
            otp_res = auth_client.verify_opt(self.FIXED_TEST_EMAIL, login_otp)
            access = otp_res.json().get("access_token") or otp_res.json().get("tokens", {}).get("access")
            
        Test_ShopStack_Product_Secure_Operations.stored_access_token = access
        self.logger.info("Vendor session verified.")

    def test_02_add_new_product(self, product_client):
        self.logger.info("Step 2: Adding new product to inventory")
        token = Test_ShopStack_Product_Secure_Operations.stored_access_token
        if not token:
            pytest.skip("Session token missing.")
            
        headers = {"Authorization": f"Bearer {token}"}
        payload = {
            "name": "Automation Smart Device",
            "price": 4999,
            "description": "Backend verification item"
        }
        
        response = product_client.add_product(payload, headers=headers)
        assert response.status_code in [200, 201]
        
        Test_ShopStack_Product_Secure_Operations.created_product_id = response.json().get("id")
        self.logger.info(f"Product added. ID: {Test_ShopStack_Product_Secure_Operations.created_product_id}")

    def test_03_delete_created_product(self, product_client):
        self.logger.info("Step 3: Removing added product from system")
        token = Test_ShopStack_Product_Secure_Operations.stored_access_token
        p_id = Test_ShopStack_Product_Secure_Operations.created_product_id
        
        if not token or not p_id:
            pytest.skip("Required parameters missing for cleanup.")
            
        headers = {"Authorization": f"Bearer {token}"}
        response = product_client.delete_product(p_id, headers=headers)
        
        assert response.status_code in [200, 204]
        self.logger.info("Product secure deletion validated successfully.")