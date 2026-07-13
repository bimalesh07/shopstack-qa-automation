import pytest
from Utilities.customLogger import LogGen

class Test_ShopStack_Products_Catalog_Public:
    logger = LogGen.apiloggen()

    extracted_product_id = None
    extracted_product_slug = None
    extracted_category_slug = None

    def test_prod_01_get_all_products(self, product_client):
        self.logger.info("Step 1: Fetching all public products")
        response = product_client.get_all_products()
        assert response.status_code == 200

        json_data = response.json()
        product_list = json_data.get("results") if isinstance(json_data, dict) else json_data
        assert len(product_list) > 0, "Catalog is empty."
        
        Test_ShopStack_Products_Catalog_Public.extracted_product_id = product_list[0].get("id")
        Test_ShopStack_Products_Catalog_Public.extracted_product_slug = product_list[0].get("slug")
        self.logger.info(f"Captured Product ID: {Test_ShopStack_Products_Catalog_Public.extracted_product_id}")

    def test_prod_02_get_product_details(self, product_client):
        self.logger.info("Step 2: Fetching product details")
        p_id = Test_ShopStack_Products_Catalog_Public.extracted_product_id
        p_slug = Test_ShopStack_Products_Catalog_Public.extracted_product_slug
        
        target = p_id if p_id is not None else p_slug
        assert target is not None, "Product identifier missing."
        
        response = product_client.get_product_by_id(target)
        if response.status_code == 404 and p_slug:
            response = product_client.get_product_by_id(p_slug)
                    
        assert response.status_code == 200
        self.logger.info(f"Verified product: {response.json().get('name')}")

    def test_prod_03_get_all_categories(self, product_client):
        self.logger.info("Step 3: Fetching product categories")
        response = product_client.get_all_categories()
        assert response.status_code == 200

        json_data = response.json()
        category_list = json_data.get("results") if isinstance(json_data, dict) else json_data
        assert len(category_list) > 0
        
        Test_ShopStack_Products_Catalog_Public.extracted_category_slug = category_list[0].get("slug") or category_list[0].get("id")
        self.logger.info(f"Captured Category Key: {Test_ShopStack_Products_Catalog_Public.extracted_category_slug}")

    def test_prod_04_filter_by_category(self, product_client):
        self.logger.info("Step 4: Filtering catalog by category key")
        c_id = Test_ShopStack_Products_Catalog_Public.extracted_category_slug
        assert c_id is not None
        
        my_params = {"category": c_id}
        response = product_client.get_all_products(params=my_params)
        assert response.status_code == 200
        self.logger.info("Category filtering verified successfully.")