import time
import os
import pytest
from .basetest import BaseTest
from PageObjects.AddCartPage import AddCartPage
from PageObjects.LoginPage import LoginPage
from PageObjects.ProductCartPage import ProductCartPage 
from Utilities.customLogger import LogGen
from PageObjects.CheckoutPage import CheckoutPage

class Test_End_To_End_Checkout(BaseTest):
    user_email = os.getenv("LOGIN_USERNAME") or "bimaleshy49@gmail.com"
    user_password = os.getenv("LOGIN_PASSWORD") or "Password@123"
    logger = LogGen.loggen()

    def _execute_user_authentication(self):
        """Step 1: Execute valid user authentication sequence and pass OTP check."""
        self.logger.info("Executing Step 1: User Authentication Sequence")
        lp = LoginPage(self.driver)
        lp.click_navbar_login()
        lp.login_direct(self.user_email, self.user_password)
        
        self.logger.info("Pausing execution for manual OTP entry on the browser screen...")
        time.sleep(20)  # OTP fill karne ka time mila
        
        assert lp.is_logout_button_visible() is True, "Validation check failed: Active login session tracking missing."
        self.logger.info("User login successfully verified.")


    def _execute_add_product_to_cart(self):
        """Step 2: Navigate to shop module, open details, and add the target item to cart."""
        self.logger.info("Executing Step 2: Catalog Navigation and Cart Inclusion")
        pc = ProductCartPage(self.driver)
        pc.navigate_to_shop_page()
        pc.click_product_to_open_details()

        ac = AddCartPage(self.driver)
        ac.add_to_cart(1)
        time.sleep(2)
        
        toast_success = ac.get_toast_message_text()
        assert toast_success is not None, "Validation check failed: Success toast notification did not display."
        
        toast_lower = toast_success.lower()
        if "added" in toast_lower or "to cart" in toast_lower or "success" in toast_lower:
            self.logger.info(f"Step A passed (Fresh Cart State): Items added successfully -> {toast_success}")
        elif "sorry" in toast_lower or "stock" in toast_lower or "only" in toast_lower or "available" in toast_lower:
            self.logger.warning(f"Step A warning (Stale Cart State): Cart already populated from a previous run -> {toast_success}")
            assert True 
        else:
            assert False, f"Validation check failed: Unexpected toast string captured in Step A: {toast_success}"

    def _execute_shipping_address_configuration(self):
        """Step 3: Redirect to shopping cart context and manage shipping layout coordinates."""
        self.logger.info("Executing Step 3: Shopping Cart Redirection and Shipping Setup")
        chk = CheckoutPage(self.driver)
        
        self.driver.get("https://shop-stack-ecommerce.vercel.app/cart")
        time.sleep(2)
        
        chk.click_checkout_securely()
        chk.wait_for_check_out_laoder_disapaer()

        self.logger.info("Handling shipping address selection or generation parameters")
        chk.handle_shipping_address(
            "Bimalesh",
            "9864378899",
            "arekre kotam atm",
            "Bengluru",
            "Arekere",
            "560076"
        )

    def _execute_payment_and_order_placement(self):
        """Step 4: Execute payment methodology allocation and validate final order placement status."""
        self.logger.info("Executing Step 4: Payment Routing and Order Verification")
        chk = CheckoutPage(self.driver)
        payment_choice = "COD"
        
        if payment_choice == "COD":
            self.logger.info("Selecting payment methodology: Cash On Delivery")
            chk.selected_payment_and_place_order()
        else:
            self.logger.info("Selecting payment methodology: Online Transaction")
            chk.selected_payment_and_place_order(method="ONLINE")
        
        time.sleep(5)

        order_status = chk.get_order_status_text()
        order_status_lower = order_status.lower()
        self.logger.info(f"Captured UI order confirmation node: {order_status}")

        assert "placed" in order_status_lower or "confirmation" in order_status_lower, \
            f"Validation check failed: System landed on incorrect routing node: {order_status}"


    def test_complete_e2e_checkout_flow(self, fresh_url):
        self.logger.info("========= STARTING MAIN E2E CHECKOUT SUITE =========")
        
        # Line-by-line saare steps ek hi browser window mein chalenge makkhan ki tarah!
        self._execute_user_authentication()
        self._execute_add_product_to_cart()
        self._execute_shipping_address_configuration()
        self._execute_payment_and_order_placement()
        
        self.logger.info("========= E2E PIPELINE PASSED COMPLETELY RESUME =========")