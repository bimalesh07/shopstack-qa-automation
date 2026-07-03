import pytest
from Utilities.customLogger import LogGen

class Test_ShopStack_Products_CataLog_Endpoints:
    
    logger = LogGen.apiloggen()
    
    extracted_product_id = None
    extracted_product_slug = None
    extracted_category_slug = None

    def test_prod_01_get_all_products_validation(self, product_client):
        self.logger.info("Starting test: Fetch all products catalog")

        response = product_client.get_all_products()
        assert response.status_code == 200

        json_data = response.json()
        product_list = json_data.get("results") if isinstance(json_data, dict) else json_data

        assert len(product_list) > 0, "Error: Product list is empty"
        
        Test_ShopStack_Products_CataLog_Endpoints.extracted_product_id = product_list[0].get("id")
        Test_ShopStack_Products_CataLog_Endpoints.extracted_product_slug = product_list[0].get("slug")
        
        self.logger.info(f"Catalog loaded successfully. Captured ID: {Test_ShopStack_Products_CataLog_Endpoints.extracted_product_id}")

    def test_prod_02_get_product_details_by_id(self, product_client):
        self.logger.info("Starting test: Get single product details")

        p_id = Test_ShopStack_Products_CataLog_Endpoints.extracted_product_id
        p_slug = Test_ShopStack_Products_CataLog_Endpoints.extracted_product_slug
        
        target = p_id if p_id is not None else p_slug
        assert target is not None, "Skipping test: No product identifier found"
        
        self.logger.info(f"Fetching details with identifier: {target}")
        response = product_client.get_product_by_id(target)
        
        if response.status_code == 404 and p_slug:
            self.logger.warning(f"ID returned 404. Retrying with fallback slug: {p_slug}")
            response = product_client.get_product_by_id(p_slug)
                    
        assert response.status_code == 200, "Details API failed for both ID and Slug"
        
        detail_data = response.json()
        self.logger.info(f"Product details verified for name: {detail_data.get('name')}")

    def test_prod_03_get_all_category(self, product_client):
        self.logger.info("Starting test: Fetch all categories")
        
        try:
            response = product_client.get_all_categories()
        except AttributeError:
            response = product_client.get_all_categrories()
            
        assert response.status_code == 200

        json_data = response.json()
        category_list = json_data.get("results") if isinstance(json_data, dict) else json_data

        assert len(category_list) > 0, "Error: No categories found"
        
        Test_ShopStack_Products_CataLog_Endpoints.extracted_category_slug = category_list[0].get("slug") or category_list[0].get("id")
        self.logger.info(f"Categories loaded. Captured category key: {Test_ShopStack_Products_CataLog_Endpoints.extracted_category_slug}")

    def test_prod_4_filter_product_by_category(self, product_client):
        self.logger.info("Starting test: Filter products by category")
        
        c_id = Test_ShopStack_Products_CataLog_Endpoints.extracted_category_slug
        assert c_id is not None, "Skipping test: No category key available"

        my_params = {"category": c_id}
        response = product_client.get_all_products(params=my_params)
        
        assert response.status_code == 200
        self.logger.info(f"Products filtered successfully for category key: {c_id}")