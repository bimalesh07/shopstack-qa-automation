import pytest
from Utilities.customLogger import LogGen

class Test_ShopStack_Product_Secure_Workflow:
    logger = LogGen.apiloggen()

    created_product_id = None

    def test_prod_01_add_product_authorized(self, product_client, user_token):
        self.logger.info("Step 1: Adding a new product using centralized conftest token")
        
      
        headers = {
            "Authorization": f"Bearer {user_token}"
        }
        
        product_payload = {
            "name": "Automation Smart Watch 2026",
            "price": 8999,
            "description": "High-end corporate testing watch"
        }
        
        response = product_client.add_product(product_payload, headers=headers)
        assert response.status_code in [200, 201]
        
  
        Test_ShopStack_Product_Secure_Workflow.created_product_id = response.json().get("id")
        self.logger.info(f"Product successfully added. ID: {Test_ShopStack_Product_Secure_Workflow.created_product_id}")

    def test_prod_02_delete_product_authorized(self, product_client, user_token):
        self.logger.info("Step 2: Cleaning up and deleting the created product")
        p_id = Test_ShopStack_Product_Secure_Workflow.created_product_id
        
        if not p_id:
            pytest.skip("Created Product ID is missing. Skipping delete test.")
            
        headers = {
            "Authorization": f"Bearer {user_token}"
        }
        
        response = product_client.delete_product(p_id, headers=headers)
        assert response.status_code in [200, 204]
        self.logger.info("Product secure deletion validated successfully.")