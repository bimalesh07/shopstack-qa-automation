import requests

class ProductEndpoints:
    def __init__(self, base_url):
        self.base_url = base_url
    
    def get_all_products(self, params=None, headers=None):
        url = f"{self.base_url}/products/"
        return requests.get(url, params=params, headers=headers)
    
    def get_product_by_id(self, product_id, headers=None):
        url = f"{self.base_url}/products/{product_id}/"
        return requests.get(url, headers=headers)
    
    def get_all_categories(self, headers=None):
        url = f"{self.base_url}/products/categories/"
        return requests.get(url, headers=headers)
   
    def add_product(self, payload, headers):
        url = f"{self.base_url}/products/add/"
        return requests.post(url, json=payload, headers=headers)


    def delete_product(self, product_id, headers):
        url = f"{self.base_url}/products/{product_id}/delete/"
        return requests.delete(url, headers=headers)