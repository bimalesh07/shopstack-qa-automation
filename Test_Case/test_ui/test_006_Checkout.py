import time
import os
from .basetest import BaseTest
from PageObjects.AddCartPage import AddCartPage
from PageObjects.LoginPage import LoginPage
from PageObjects.ProductCartPage import ProductCartPage 
from Utilities.customLogger import LogGen
from PageObjects.CheckoutPage import CheckoutPage

class Test_End_To_End_Checkout(BaseTest):
    user_email = os.getenv("LOGIN_USERNAME") if os.getenv("LOGIN_USERNAME") else "bimaleshy49@gmail.com"
    user_password = os.getenv("LOGIN_PASSWORD") if os.getenv("LOGIN_PASSWORD") else "Password@123"
    logger = LogGen.loggen()

    def test_checkout_and_place_order_flow(self):
        self.logger.info("**************Starting Checkout and Order Placement Test")
        lp = LoginPage(self.driver)
        lp.click_navbar_login()
        lp.login_direct(self.user_email, self.user_password)
        self.logger.info("Wating For OTP Manualy")
        time.sleep(20)
        assert lp.is_logout_button_visible() == True, "ERROR: Not Login Successfully "

        """Add to product to cart """
        pc = ProductCartPage(self.driver)
        pc.navigate_to_shop_page()
        pc.click_product_to_open_details()

        ac = AddCartPage(self.driver)
        ac.add_to_cart(1)
        time.sleep(2)
        # Toast assertion block
        toast_success = ac.get_toast_message_text()
        assert toast_success is not None, "Test Failed: Success toast notification did not show"
        
        toast_lower = toast_success.lower()
        
        if "added" in toast_lower or "to cart" in toast_lower or "success" in toast_lower:
            self.logger.info(f"STEP A PASSED (Fresh Cart State): Items added successfully -> {toast_success}")
            
        elif "sorry" in toast_lower or "stock" in toast_lower or "only" in toast_lower or "available" in toast_lower:
            self.logger.warning(f"STEP A PASSED (Stale Cart State): Cart already full from previous run -> {toast_success}")
            assert True 
        else:
            assert False, f"Test Failed: Unexpected toast string captured in Step A: {toast_success}"

        """Redirection cart page """
        chk = CheckoutPage(self.driver)
        self.logger.info("Clicking the Secure Checkout")
        self.driver.get("https://shop-stack-ecommerce.vercel.app/cart")
        time.sleep(2)
        chk.click_checkout_securely()
        chk.wait_for_check_out_laoder_disapaer()


        """Add Address When there are not address """
        self.logger.info("Hashing shipping address selection/creation")

        chk.handle_shipping_address(
            "Bimalesh",
            "9864378899",
            "arekre kotam atm",
            "Bengluru",
            "Arekere",
            "560076"
        )

        """Dymanic overwrite choice"""
        payment_choice = "COD"
        self.logger.info("PAYENT COD")
        if payment_choice =="COD":
            chk.selected_payment_and_place_order()
        else:
            chk.selected_payment_and_place_order(method="ONLINE")
        
        time.sleep(5)

        """Order placed """
        order_status = chk.get_order_status_text()
        order_staus_lower = order_status.lower()
        self.logger.info(f"Captured order_Status:'{order_status}'")

        assert "placed" in order_staus_lower or "confirmation" in order_staus_lower, \
            f"❌ Test Failed: Automation landed on incorrect routing node: '{order_status}'"
        
        self.logger.info("*********** END SUITE: ORDER PLACEMENT TEST 100% PASSED ***********")

    





