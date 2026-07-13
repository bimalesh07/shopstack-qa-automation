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
        self.logger.info("Step 1: User Login Validation")
        lp = LoginPage(self.driver)
        lp.click_navbar_login()
        lp.login_direct(self.user_email, self.user_password)

        self.logger.info("Waiting for manual OTP...")
        time.sleep(15)
        
        assert lp.is_logout_button_visible() is True, "Login session failed."
        self.logger.info("User login successfully verified.")

    def test_02_apply_shop_filters(self):
        self.logger.info("Step 2: Apply Shop Filters")
        sp = ProductCartPage(self.driver)
        sp.navigate_to_shop_page()

        sp.apply_reactive_price_filters("300", "2000")

        self.logger.info("Verifying active price filters...")
        reset_visible = sp.wait.until(
            lambda d: d.find_element(By.XPATH, sp.button_reset_filters_xpath).is_displayed()
        )
        assert reset_visible is True, "Filter layout state mismatch."
        self.logger.info("Price filters applied successfully.")

        sp.apply_sorting_filter("low to high")
        self.logger.info("Sorting filter updated to Low to High.")

    def test_03_wishlist_and_product_details(self):
        self.logger.info("Step 3: Wishlist and Product Details Validation")
        sp = ProductCartPage(self.driver)

        self.logger.info("Verifying wishlist interaction...")
        toast_message_text = sp.click_wishlist_heart_and_capture_toast()
        
        assert "added" in toast_message_text.lower() or "wishlist" in toast_message_text.lower(), \
            f"Unexpected wishlist toast: '{toast_message_text}'"
        self.logger.info("Wishlist verification successful.")

        sp.click_product_to_open_details()

        self.logger.info("Verifying product details redirection...")
        redirection_proof = sp.is_details_page_opened_successfully()

        assert redirection_proof is True, "Product details view failed to open."
        self.logger.info("Product details page verified.")
        self.logger.info("Shop module workflow completed.")