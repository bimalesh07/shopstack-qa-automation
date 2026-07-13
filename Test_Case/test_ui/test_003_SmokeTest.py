import time
import pytest
from .basetest import BaseTest
from PageObjects.HomePage import ProductPage
from Utilities.customLogger import LogGen

class Test_003_Guest_Smoke_Flows(BaseTest):
    logger = LogGen.loggen()

    def test_guest_complete_smoke_journey(self, fresh_url):
        self.logger.info(" Guest Complete Smoke Journey")
        
        prod = ProductPage(self.driver)

        prod.click_dark_mode()
        time.sleep(3)
        prod.click_light_mode()
        time.sleep(3)
     
        prod.open_collections_dropdown()
        time.sleep(3)
        
     
        prod.click_shop_navigation()
        time.sleep(2)
        
      
        prod.serach_product("Laptop")
        time.sleep(3)
        
        
        prod.click_heart_icon()
        time.sleep(2)
        assert prod.is_login_page_enforced() is True, "Login redirection screen not initialized."
        self.logger.info("Verified guest access constraints enforced for wishlist interaction.")

        self.driver.get("https://shopstack-ecommerce.vercel.app/products")
        time.sleep(2)

    
        prod.click_first_listed_product()
        time.sleep(3)
        assert self.driver.find_element("xpath", prod.text_product_title_xpath).is_displayed() is True, \
            " Product description landing lookup failed."
        self.logger.info("Target metadata loaded successfully in guest session.")
        
       
        prod.click_secure_checkout()
        time.sleep(3)
        assert prod.is_login_page_enforced() is True, "Checkout action leaked bypass constraints."
        self.logger.info("Guest smoke suite validation execution completed successfully.")