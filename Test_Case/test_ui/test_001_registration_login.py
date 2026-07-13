import os
import time
import random
import pytest

from .basetest import BaseTest
from PageObjects.RegistrationPage import RegistrationPage
from Utilities.customLogger import LogGen


class Test__001_User_Registration_Suite(BaseTest):
    logger = LogGen.loggen()
    
    c_name = os.getenv("CUSTOMER_NAME") or "Kamalesh Yadav"
    c_email = os.getenv("CUSTOMER_EMAIL") or "bimaleshk07@gmail.com"
    c_phone = os.getenv("CUSTOMER_PHONE") or "+917050863365"
    c_password = os.getenv("CUSTOMER_PASSWORD") or "SecurePass@123"

    v_name = os.getenv("VENDOR_NAME") or "Bhai Vendor Store"
    v_email = os.getenv("VENDOR_EMAIL") or "vendor_bhai_temp@mailinator.com"
    v_phone = os.getenv("VENDOR_PHONE") or "+919123456789"
    v_password = os.getenv("VENDOR_PASSWORD") or "VendorPassword@123"
    v_shop = os.getenv("VENDOR_SHOP_NAME") or "Bhai Ki Digital Dukaan"
    v_desc = os.getenv("VENDOR_SHOP_DESC") or "We sell items fast."

    def test_01_registration_blank_fields_validation(self, fresh_url):
        self.logger.info("Registration Blank Fields Validation")
        rp = RegistrationPage(self.driver)
        rp.login_btn()
        rp.got_to_signup_page()
        rp.select_role("Customer")
        
        rp.fill_Registration_from("customer", "", "", "", "")
        rp.click_create_account("customer")
        time.sleep(1)
        
        error_text = rp.get_any_validation_error_text(field_type="name").lower()
        
        assert "fill" in error_text or "required" in error_text, f"Validation check failed: {error_text}"
        assert rp.is_registration_successful("customer") is False
        self.logger.info("HTML5 native validation successfully blocked blank data entry.")

    def test_02_customer_registration_invalid_email(self, fresh_url):
        self.logger.info("Customer Registration Invalid Email Format")
        rp = RegistrationPage(self.driver)
        rp.login_btn()
        rp.got_to_signup_page()
        rp.select_role("customer")
        
        rp.fill_Registration_from("customer", "gfgfg", "gfg", "1234567890", "Secure@123")
        rp.click_create_account("customer")
        time.sleep(1)
        
        error_text = rp.get_any_validation_error_text(field_type="email").lower()
        
        assert "include" in error_text or "@" in error_text, f"Validation check failed: {error_text}"
        assert rp.is_registration_successful("customer") is False
        self.logger.info("Test passed: HTML5 validation successfully caught missing '@' parameter.")

    def test_03_customer_registration_missing_password(self, fresh_url):

        self.logger.info("Executing test case: Customer Registration Missing Password")
        rp = RegistrationPage(self.driver)
        rp.login_btn()
        rp.got_to_signup_page()
        rp.select_role("customer")
        
        rp.fill_Registration_from("customer", "gfgfg", "bimaleshk07@gmail.com", "1234567890", "")
        rp.click_create_account("customer")
        time.sleep(1)
        
        error_text = rp.get_any_validation_error_text(field_type="password").lower()
        
        assert "fill" in error_text or "required" in error_text, f"Validation check failed: {error_text}"
        assert rp.is_registration_successful("customer") is False
        self.logger.info("HTML5 native tooltip blocked submission due to empty password.")

    def test_04_customer_registration_positive(self):
        self.logger.info("Customer Registration Positive Flow")
        rp = RegistrationPage(self.driver)
        rp.login_btn()
        rp.got_to_signup_page()
        rp.select_role("customer")
        
        rp.fill_Registration_from("customer", self.c_name, self.c_email, self.c_phone, self.c_password)
        rp.click_create_account("customer")
        
        self.logger.info("Pausing execution for manual OTP entry on the browser screen...")
        time.sleep(25) 
        time.sleep(3)

        reg_status = rp.is_registration_successful("customer")
        assert reg_status is True, "Profile button element not found."
        self.logger.info("Registration verified via successful profile button appearance.")