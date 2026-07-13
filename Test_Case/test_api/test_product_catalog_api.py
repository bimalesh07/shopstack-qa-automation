import pytest
from Utilities.customLogger import LogGen

class Test_ShopStack_Products_CataLog_Endpoints:
    logger = LogGen.apiloggen()
    extracted_product_id = None
    extracted_product_slug = None
    extracted_category_slug = None

    def test_prod_01_get_all_products_validation(self, product_client):
        self.logger.info("Step 1: Fetch All Products")

        response = product_client.get_all_products()
        assert response.status_code == 200

        json_data = response.json()
        product_list = json_data.get("results") if isinstance(json_data, dict) else json_data

        assert len(product_list) > 0, "Product list is empty."
        
        Test_ShopStack_Products_CataLog_Endpoints.extracted_product_id = product_list[0].get("id")
        Test_ShopStack_Products_CataLog_Endpoints.extracted_product_slug = product_list[0].get("slug")
        
        self.logger.info(f"Product list loaded. Captured ID: {Test_ShopStack_Products_CataLog_Endpoints.extracted_product_id}")

    def test_prod_02_get_product_details_by_id(self, product_client):
        self.logger.info("Step 2: Get Product Details")

        p_id = Test_ShopStack_Products_CataLog_Endpoints.extracted_product_id
        p_slug = Test_ShopStack_Products_CataLog_Endpoints.extracted_product_slug
        
        target = p_id if p_id is not None else p_slug
        assert target is not None, "Product identifier missing."
        
        self.logger.info(f"Fetching product details for: {target}")
        response = product_client.get_product_by_id(target)
        
        if response.status_code == 404 and p_slug:
            self.logger.warning(f"Retrying with fallback slug: {p_slug}")
            response = product_client.get_product_by_id(p_slug)
                    
        assert response.status_code == 200, "Product details API failed."
        
        detail_data = response.json()
        self.logger.info(f"Product verified: {detail_data.get('name')}")

    def test_prod_03_get_all_category(self, product_client):
        self.logger.info("Step 3: Fetch All Categories")
        
        # 🎯 Agar product_client mein spelling mistake theek kar li hai, toh ye direct chalega
        response = product_client.get_all_categories()
        assert response.status_code == 200

        json_data = response.json()
        category_list = json_data.get("results") if isinstance(json_data, dict) else json_data

        assert len(category_list) > 0, "No categories found."
        
        Test_ShopStack_Products_CataLog_Endpoints.extracted_category_slug = category_list[0].get("slug") or category_list[0].get("id")
        self.logger.info(f"Categories loaded. Captured key: {Test_ShopStack_Products_CataLog_Endpoints.extracted_category_slug}")

    def test_prod_4_filter_product_by_category(self, product_client):
        self.logger.info("Step 4: Filter Products by Category")
        
        c_id = Test_ShopStack_Products_CataLog_Endpoints.extracted_category_slug
        assert c_id is not None, "Category key missing."

        my_params = {"category": c_id}
        response = product_client.get_all_products(params=my_params)
        
        assert response.status_code == 200
        self.logger.info(f"Products successfully filtered for category: {c_id}")