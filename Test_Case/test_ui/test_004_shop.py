
import time
import os
from .basetest import BaseTest
from PageObjects.ProductCartPage import ProductCartPage
from PageObjects.LoginPage import LoginPage
from Utilities.customLogger import LogGen
from selenium.webdriver.common.by import By

class Test_004_Shop_Validation(BaseTest):
    logger = LogGen.loggen()
    user_email = os.getenv("LOGIN_USERNAME") if os.getenv("LOGIN_USERNAME") else "bimaleshy49@gmail.com"
    user_password = os.getenv("LOGIN_PASSWORD") if os.getenv("LOGIN_PASSWORD") else "Password@123"

    def test_04_full_shop_page(self):
        self.logger.info("*********** START SUITE: LOGIN AND SHOP MODULE ***********")
        
        # 🔑 STAGE 1: AUTHORIZATION PRE-REQUISITE
        self.logger.info("Step 1: Running direct valid authorization sequence...")
        lp = LoginPage(self.driver)
        lp.click_navbar_login()
        lp.login_direct(self.user_email, self.user_password)

        self.logger.info("⏳ MANUAL ACTION REQUIRED: Enter OTP right now in browser window...")
        time.sleep(15)
        assert lp.is_logout_button_visible() == True, "❌ Critical Break: Active login session tracking missing!"

        self.logger.info("🟢 Session confirmed! Navigating to shop page context...")

        # 🛒 STAGE 2: SHOP PAGE MODULE PIPELINE
        self.logger.info("Step 2: Triggering shop module functional features...")
        sp = ProductCartPage(self.driver)
        sp.navigate_to_shop_page()

        # Input reactive price range parameters
        sp.apply_reactive_price_filters("300", "2000")

        # Validation Proof 1: Verify filter implementation state using Reset button anchor
        self.logger.info("🔬 Investigating validation anchors for active price filters...")
        reset_visible = sp.wait.until(
            lambda d: d.find_element(By.XPATH, sp.button_reset_filters_xpath).is_displayed()
        )
        assert reset_visible == True, "❌ Saboot 1 Failed: Filter layout engine state mismatch!"
        self.logger.info("🟢 PROOF 1 PASSED: Reactive price filters state updated cleanly on screen.")

        # Trigger dynamic sorting engine
        sp.apply_sorting_filter("low to high")
        self.logger.info("🟢 Sorting modification parameter updated to Low to High.")

        # Validation Proof 2: Wishlist transaction alert validation
        self.logger.info("🔬 Investigating Wishlist heart interaction feedback text node...")
        toast_message_text = sp.click_wishlist_heart_and_capture_toast()
        
        assert "added" in toast_message_text.lower() or "wishlist" in toast_message_text.lower(), \
            f"❌ Saboot 2 Failed: Toast text node validation mismatch! Captured: '{toast_message_text}'"
        self.logger.info("🟢 PROOF 2 PASSED: Wishlist transaction verified via overlay notification toast.")

        # Step into single product view details layer
        sp.click_product_to_open_details()

        # Validation Proof 3: Details landing page landmark validation
        self.logger.info("🔬 Investigating Product Details Page redirection landmark element structure...")
        redirection_proof = sp.is_details_page_opened_successfully()

        assert redirection_proof == True, "❌ Saboot 3 Failed: Target product details view layout expansion broke!"
        self.logger.info("🟢 PROOF 3 PASSED: Product details page redirection confirmed by landmark elements.")

        self.logger.info("🎉 SUCCESSFUL SUITE: Full independent Shop Module stack evaluated with 100% precision!")