# File: PageObjects/LoginPage.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utilities.customLogger import LogGen
import time

class LoginPage:
    # 🎯 1. Navbar Login Button
    button_navbar_login_xpath = "//span[@class='hidden md:block']"
    
    # 🎯 2. Login Form Fields
    textbox_email_xpath = "//input[@placeholder='you@example.com']"
    textbox_password_xpath = "//input[@type='password']"
    button_signin_xpath = "//button[@type='submit']"
    
    # 🎯 3. Validations & Dynamic Popups
    text_login_error_xpath = "//div[contains(@class,'text-rose-600') or contains(text(),'invalid') or contains(text(),'password')]"
    
    # Fix: Corrected variable name ('BK' avatar button based on screenshot)
    button_user_avatar_xpath = "//button[contains(., 'BK') or contains(@class, 'rounded-full')]"
    
    # Fix: Corrected broken Logout XPath
    button_logout_xpath = "//button[contains(text(),'Logout') or contains(.,'LOGOUT')] | //span[contains(text(),'Logout')]"

    def __init__(self, driver):
        self.driver = driver
        self.logger = LogGen.loggen()
        self.wait = WebDriverWait(self.driver, 15)

    def click_navbar_login(self):
        self.logger.info("👉 Clicking NAVBAR LOGIN button from homepage...")
        element = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.button_navbar_login_xpath)))
        self.driver.execute_script("arguments[0].click();", element)

    def login_direct(self, email, password):
        email_field = self.wait.until(EC.presence_of_element_located((By.XPATH, self.textbox_email_xpath)))
        email_field.clear()
        if email: email_field.send_keys(email)
        
        pass_field = self.driver.find_element(By.XPATH, self.textbox_password_xpath)
        pass_field.clear()
        if password: pass_field.send_keys(password)

        self.logger.info("🚀 Clicking Sign In Form Submit Button...")
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.button_signin_xpath))).click()

    def get_login_error_text(self):
        try:
            self.logger.info("⏳ Waiting for backend error validation message alert...")
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, self.text_login_error_xpath))
            )
            return element.text
        except Exception as e:
            self.logger.error("⚠️ Error block locator timeout.")
            return ""

    def is_logout_button_visible(self):
        self.logger.info("🔍 Step 1: Checking if User Profile Avatar (BK) is painted on dashboard...")
        try:
            local_wait = WebDriverWait(self.driver, 12)
            
            # Locate avatar
            avatar_btn = local_wait.until(
                EC.element_to_be_clickable((By.XPATH, self.button_user_avatar_xpath))
            )
            self.logger.info("🎯 Profile Avatar found! Clicking it to open dynamic dropdown menu...")
            self.driver.execute_script("arguments[0].click();", avatar_btn)
            
            time.sleep(1.5) # Wait for dropdown slide transition
            
            # Check dynamic Logout
            logout_btn = local_wait.until(
                EC.visibility_of_element_located((By.XPATH, self.button_logout_xpath))
            )
            
            if logout_btn.is_displayed():
                self.logger.info("🎯 Success: LOGOUT button component is strictly visible inside dropdown menu.")
                # Close the dropdown menu to avoid blocking the SHOP link click
                self.logger.info("🔄 Closing the profile dropdown menu to clear the UI overlay...")
                self.driver.execute_script("arguments[0].click();", avatar_btn)
                time.sleep(1) # Small stabilization wait for menu to close
                
                return True
            
            return False  
        
        except Exception as e:
            self.logger.warning("⚠️ Component Timeout: User is not logged in or avatar menu didn't open.")
            return False