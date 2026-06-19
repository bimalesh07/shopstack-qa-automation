import os
import time
import random
import pytest

from .basetest import BaseTest
from PageObjects.RegistrationPage import RegistrationPage
from Utilities.customLogger import LogGen


class Test__001_User_Registration_Suite(BaseTest):
    logger = LogGen.loggen()
    
    # Environment mappings
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

    # 🔴 TEST 01: Blank Fields Check (Pic 1)
    def test_01_registration_blank_fields_validation(self):
        self.logger.info("Test: Customer Registration Blank Fields (Pic 1)")
        rp = RegistrationPage(self.driver)
        rp.login_btn()
        rp.got_to_signup_page()
        rp.select_role("Customer")
        
        # Send all empty fields
        rp.fill_Registration_from("customer", "", "", "", "")
        rp.click_create_account("customer")
        time.sleep(1)
        
        # Name field ka native html5 verification message uthao
        error_text = rp.get_any_validation_error_text(field_type="name").lower()
        
        # Native popup verification text check matrix
        assert "fill" in error_text or "required" in error_text, f"❌ Tooltip match failed! Got: {error_text}"
        assert rp.is_registration_successful("customer") == False
        self.logger.info("🎉 PASSED: HTML5 Native validation successfully blocked blank data entry.")

    # 🔴 TEST 02: Invalid Email Format Check (Pic 2)
    def test_02_customer_registration_invalid_email(self):
        self.logger.info("Test: Customer Registration Invalid Email (Pic 2)")
        rp = RegistrationPage(self.driver)
        rp.login_btn()
        rp.got_to_signup_page()
        rp.select_role("customer")
        
        # Sent email address without '@' symbol
        rp.fill_Registration_from("customer", "gfgfg", "gfg", "1234567890", "Secure@123")
        rp.click_create_account("customer")
        time.sleep(1)
        
        # Email field ka html5 validation text uthao
        error_text = rp.get_any_validation_error_text(field_type="email").lower()
        
        assert "include" in error_text or "@" in error_text, f"❌ Tooltip match failed! Got: {error_text}"
        assert rp.is_registration_successful("customer") == False
        self.logger.info("🎉 PASSED: HTML5 validation successfully caught missing '@' parameter.")

    # 🔴 TEST 03: Password Field Left Empty Check (Pic 3)
    def test_03_customer_registration_missing_password(self):
        self.logger.info("Test: Customer Registration Missing Password (Pic 3)")
        rp = RegistrationPage(self.driver)
        rp.login_btn()
        rp.got_to_signup_page()
        rp.select_role("customer")
        
        # Name and email filled, but password left empty
        rp.fill_Registration_from("customer", "gfgfg", "bimaleshk07@gmail.com", "1234567890", "")
        rp.click_create_account("customer")
        time.sleep(1)
        
        # Password field ka verification check uthao
        error_text = rp.get_any_validation_error_text(field_type="password").lower()
        
        assert "fill" in error_text or "required" in error_text, f"❌ Tooltip match failed! Got: {error_text}"
        assert rp.is_registration_successful("customer") == False
        self.logger.info("🎉 PASSED: HTML5 native tooltip blocked submission due to empty password.")

    # 🟢 TEST 04: Customer Positive Flow (Valid Data)
    def test_04_customer_registration_positive(self):
        self.logger.info("Test: Customer Registration Happy Path")
        rp = RegistrationPage(self.driver)
        rp.login_btn()
        rp.got_to_signup_page()
        rp.select_role("customer")
        
        # Random fresh identifier to avoid duplicate backend errors
        # random_id = random.randint(1000, 9999)
        # dynamic_email = f"BimaleshYadav_{random_id}@gmail.com"
        
        rp.fill_Registration_from("customer", self.c_name, self.c_email, self.c_phone, self.c_password)
        rp.click_create_account("customer")
        
        self.logger.info("⏳ MANUAL ACTION: Enter OTP right now on the browser screen...")
        time.sleep(25) 

        time.sleep(3)

     # 🟢 Dynamic check without text dependency (Button presence check)
        reg_status = rp.is_registration_successful("customer")
        assert reg_status == True, "❌ Dashboard verification failed: Profile Violet Button not found!"
        self.logger.info("🎉 SUCCESS: Registration verified via Profile Button appearance!")


    # # 🟢 TEST 05: Vendor Positive Flow (Valid Data)
    # def test_05_vendor_registration_positive(self):
    #     self.logger.info("Test: Vendor Registration Happy Path")
    #     rp = RegistrationPage(self.driver)
    #     rp.login_btn()
    #     rp.got_to_signup_page()
    #     rp.select_role("vendor")
        
    #     # random_id = random.randint(1000, 9999)
    #     # dynamic_email = f"vendor_bhai_{random_id}@gmail.com"
        
    #     rp.fill_Registration_from("vendor", self.v_name, self.c_email, self.v_phone, self.v_password, shop_name=self.v_shop, shop_dec=self.v_desc)
    #     rp.click_create_account("vendor")

    #     self.logger.info("⏳ MANUAL ACTION: Enter OTP for Vendor interface verification...")
    #     time.sleep(25)

    #     time.sleep(3)

    #     # Passing role string to cross-examine target interface 'Add Product' element
    #     assert rp.is_registration_successful("vendor") == True, "❌ Vendor validation with 'Add Product' dashboard component failed!"
    #     self.logger.info("🎉 PASSED: Vendor layout access confirmed via 'Add Product' element.")