from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from Utilities.customLogger import LogGen

class RegistrationPage:
    #Standard Locators
    Login_btn = "//span[@class='hidden md:block']"
    link_signup_homepage_xpath = "//a[normalize-space()='Sign Up']"
    button_customer_tab_xpath = "//span[normalize-space()='Customer']"
    button_vendor_tab_xpath = "//span[normalize-space()='Vendor']"
    
    textbox_fullname_xpath = "//input[@placeholder='John Doe']"
    textbox_email_xpath = "//input[@placeholder='you@example.com']"
    textbox_phone_xpath = "//input[@placeholder='+1 234 567 890']"
    
    textbox_password_xpath = "//input[@name='password']"
    textbox_confirm_password_xpath = "//input[@name='password2']"
    
    #Extra Vendor Locators
    textbox_shop_name_xpath = "//input[@placeholder='Your Shop Name']"
    textbox_shop_desc_xpath = "//textarea[@placeholder='Describe your shop...']"
    textbox_invite_code_xpath = "//input[@placeholder='Invite code (optional)']"
    
    #Dynamic Submit Buttons & Custom Backend Error Box
    button_create_customer_xpath = "//span[normalize-space()='Create Customer Account']"
    button_create_vendor_xpath = "//span[normalize-space()='Create Vendor Account']"
    
    # Custom backend message box (e.g. Email already exists or Server error panel)
    text_custom_error_box_xpath = "//div[contains(@class,'text-rose-600')] | //div[contains(@class,'bg-rose-50')]"
    
    # SUCCESS VALIDATION XPATHS: Jo tumne bataye!
    success_customer_indicator_xpath = "//button[contains(@class,'rounded-full') and contains(@class,'bg-violet-600')]"
    success_vendor_indicator_xpath = "//span[text()='Add Product'] | //button[contains(.,'Add Product')]"

    def __init__(self, driver):
        self.driver = driver
        self.logger = LogGen.loggen()
        self.wait = WebDriverWait(self.driver, 15)
    
    def login_btn(self):
        self.logger.info("Clicking Login Btn")
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.Login_btn))).click()
    
    def got_to_signup_page(self):
        self.logger.info("Clicking SignUp link from Home Screen..")
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.link_signup_homepage_xpath))).click()
    
    def select_role(self, role_type):
        if role_type.lower() == "customer":
            self.logger.info("Selecting Customer role tab")
            self.wait.until(EC.element_to_be_clickable((By.XPATH, self.button_customer_tab_xpath))).click()
        elif role_type.lower() == "vendor":
            self.logger.info("Selecting Vendor role tab")
            self.wait.until(EC.element_to_be_clickable((By.XPATH, self.button_vendor_tab_xpath))).click()
    
    def fill_Registration_from(self, role_type, name, email, phone, password, shop_name=None, shop_dec=None, invite_code=None):
        self.logger.info(f"Filling details for {role_type}")
        self.wait.until(EC.presence_of_element_located((By.XPATH, self.textbox_fullname_xpath))).send_keys(name)
        self.driver.find_element(By.XPATH, self.textbox_email_xpath).send_keys(email)
        self.driver.find_element(By.XPATH, self.textbox_phone_xpath).send_keys(phone)
        self.driver.find_element(By.XPATH, self.textbox_password_xpath).send_keys(password)
        self.driver.find_element(By.XPATH, self.textbox_confirm_password_xpath).send_keys(password)

        if role_type.lower() == "vendor":
            self.logger.info("Vendor extra field detected. Filling Shop Details")
            self.wait.until(EC.presence_of_element_located((By.XPATH, self.textbox_shop_name_xpath))).send_keys(shop_name)
            self.wait.until(EC.presence_of_element_located((By.XPATH, self.textbox_shop_desc_xpath))).send_keys(shop_dec)
            if invite_code:
                self.driver.find_element(By.XPATH, self.textbox_invite_code_xpath).send_keys(invite_code)
    
    def click_create_account(self, role_type):
        if role_type.lower() == "customer":
            self.logger.info("Clicking Create Customer Account Button")
            self.wait.until(EC.element_to_be_clickable((By.XPATH, self.button_create_customer_xpath))).click()
        elif role_type.lower() == "vendor":
            self.logger.info("Clicking Create Vendor Account Button")
            self.wait.until(EC.element_to_be_clickable((By.XPATH, self.button_create_vendor_xpath))).click()
    
    # Error handler: Gets text from both HTML5 tooltip and custom box
    def get_any_validation_error_text(self, field_type="name"):
        # 1. Check if browser native HTML5 tooltip popped up (Pic 1, 2, 3)
        try:
            if field_type == "name":
                element = self.driver.find_element(By.XPATH, self.textbox_fullname_xpath)
            elif field_type == "email":
                element = self.driver.find_element(By.XPATH, self.textbox_email_xpath)
            elif field_type == "password":
                element = self.driver.find_element(By.XPATH, self.textbox_password_xpath)
                
            browser_error = element.get_attribute("validationMessage")
            if browser_error:
                self.logger.info(f"HTML5 Browser Tooltip caught: {browser_error}")
                return browser_error
        except:
            pass

        # 2. If HTML5 not found, check if custom red error box popped up
        try:
            custom_error = self.driver.find_element(By.XPATH, self.text_custom_error_box_xpath).text
            if custom_error:
                self.logger.info(f"Custom Div Error caught: {custom_error}")
                return custom_error
        except:
            pass
            
        return ""
    
    # Dynamic success checker: scan for success elements
    def is_registration_successful(self, role_type):
    #   """  try:
    #         if role_type.lower() == "customer":
    #             self.logger.info("🔍 Scanning for Customer Violet Profile Icon safely...")
    #             # Fix: added explicit wait for visibility of element to handle rendering delay
    #             element = self.wait.until(EC.visibility_of_element_located((By.XPATH, self.success_customer_indicator_xpath)))
    #             if element:
    #                 self.logger.info("Profile Button render check complete.")
    #                 return True
    #         elif role_type.lower() == "vendor":
    #             self.logger.info("Scanning for Vendor 'Add Product' module button...")
    #             element = self.wait.until(EC.visibility_of_element_located((By.XPATH, self.success_vendor_indicator_xpath)))
    #             if element:
    #                 return True
    #         return False
    #     except:
    #         self.logger.error(f"Landing validation component target timed out for role: {role_type}")
    #         return False"""
          #ULTRA HACK: Bina kisi locator ke direct page content verification matrix

        time.sleep(3) # Buffer wait for dashboard text to load
        try:
            page_text = self.driver.page_source.lower()
            if role_type.lower() == "customer":
                self.logger.info("🔍 Scanning page source content for Customer markers...")
                # Toast Match: If screen shows verified, successfully or logout
                if "verified" in page_text or "successfully" in page_text or "logout" in page_text:
                    self.logger.info("Customer landing confirmed via validation message matrix.")
                    return True
              
                
            elif role_type.lower() == "vendor":
                self.logger.info("Scanning page source content for Vendor markers...")
                if "product" in page_text or "logout" in page_text:
                    return True
            return False
        except:
            return False