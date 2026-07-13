import time
import os
import pytest
from .basetest import BaseTest
from PageObjects.ProductCartPage import ProductCartPage
from PageObjects.LoginPage import LoginPage
from Utilities.customLogger import LogGen
from selenium.webdriver.common.by import By

class Test_004_Shop_Validation(BaseTest):
    logger = LogGen.loggen()
    
    user_email = os.getenv("LOGIN_USERNAME") or "bimaleshy49@gmail.com"
    user_password = os.getenv("LOGIN_PASSWORD") or "Password@123"

    def test_01_user_login(self, fresh_url):
        self.logger.info("Executing Step 1: User Login Validation")
        lp = LoginPage(self.driver)
        lp.click_navbar_login()
        lp.login_direct(self.user_email, self.user_password)

        self.logger.info("Pausing execution for manual OTP entry on the browser screen...")
        time.sleep(15)
        
        assert lp.is_logout_button_visible() is True, "Active login session tracking missing."
        self.logger.info("User login successfully verified.")

    def test_02_apply_shop_filters(self):
        self.logger.info("Shop Page Catalog Filters Validation")
        
        sp = ProductCartPage(self.driver)
        sp.navigate_to_shop_page()

        # Apply price range parameters
        sp.apply_reactive_price_filters("300", "2000")

        #Verify filter state using Reset button anchor
        self.logger.info("Verifying validation anchors for active price filters")
        reset_visible = sp.wait.until(
            lambda d: d.find_element(By.XPATH, sp.button_reset_filters_xpath).is_displayed()
        )
        assert reset_visible is True, "Validation check failed: Filter layout engine state mismatch."
        self.logger.info("Reactive price filters state updated cleanly on screen.")

        # Trigger sorting modification
        sp.apply_sorting_filter("low to high")
        self.logger.info("Sorting modification parameter updated to Low to High.")

    def test_03_wishlist_and_product_details(self):
        self.logger.info(" Wishlist and Product Details Layer Validation")
        
        sp = ProductCartPage(self.driver)

        #  Wishlist transaction alert validation
        self.logger.info("Verifying wishlist interaction feedback overlay notification")
        toast_message_text = sp.click_wishlist_heart_and_capture_toast()
        
        assert "added" in toast_message_text.lower() or "wishlist" in toast_message_text.lower(), \
            f"Toast notification mismatch. Captured: '{toast_message_text}'"
        self.logger.info("Wishlist transaction verified via overlay notification toast.")

        # Navigate into single product view details layer
        sp.click_product_to_open_details()

        #Details landing page landmark validation
        self.logger.info("Verifying product details page redirection landmark elements")
        redirection_proof = sp.is_details_page_opened_successfully()

        assert redirection_proof is True, "Validation check failed: Target product details view layout expansion failed."
        self.logger.info("Product details page redirection confirmed by landmark elements.")
        self.logger.info("Shop module workflow pipeline completed successfully.")