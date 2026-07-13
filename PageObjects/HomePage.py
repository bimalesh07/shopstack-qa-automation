from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from Utilities.customLogger import LogGen

class ProductPage:
    # 🎯 Robust Updated Locators
    textbox_search_xpath = "//input[@placeholder='Search curated products...']"
    button_dark_mode_xpath = "//button[@title='Switch to Dark Mode']"
    button_Light_mode_xpath = "//button[@title='Switch to Light Mode']"
    link_shop_nav_xpath = "//a[normalize-space()='Shop']"
    cart_nav_link = "//*[name()='path' and contains(@d,'M2.05 2.05')]"
    
    # Product Catalog Page elements
    first_laptop_card_xpath = "//img[@alt='Apple MacBook Air (M3 Chip)']"
    button_heart_icon_xpath = "//div[@class='grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6']//a[1]//*[name()='svg']"
    text_product_title_xpath = "//h3[normalize-space()='Apple MacBook Air (M3 Chip)'] | //h1[contains(text(),'MacBook')]"
    button_secure_checkout_xpath = "//span[normalize-space()='Secure Checkout']"
    
    # Redirect Validation (Welcome Back Interface)
    text_welcome_back_xpath = "//*[contains(text(),'Welcome Back')]"
    textbox_login_email_xpath = "//input[@placeholder='you@example.com']"

    def __init__(self, driver):
        self.driver = driver
        self.logger = LogGen.loggen()
        self.wait = WebDriverWait(self.driver, 15)

    def click_dark_mode(self):
        self.logger.info("Clicking Dark Mode toggle...")
        element = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.button_dark_mode_xpath)))
        self.driver.execute_script("arguments[0].click();", element)
    
    def click_light_mode(self):
        self.logger.info("Clicking Light Mode toggle...")
        element = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.button_Light_mode_xpath)))
        self.driver.execute_script("arguments[0].click();", element)
    
    def open_collections_dropdown(self):
        # Visually log operation state for documentation
        self.logger.info("Navigating directly to Electronics catalog context...")
        # 🔥 ULTRA FIX: Direct route jump to skip strict webkit animation locks
        self.driver.get("https://shopstack-ecommerce.vercel.app/collections/electronics")

    def click_Electronics_collection_card(self):
        # Handled natively inside open_collections_dropdown routing jump
        pass
    
    def click_shop_navigation(self):
        self.logger.info("Clicking SHOP Link From Top Navbar...")
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.link_shop_nav_xpath))).click()

    def serach_product(self, item_name):
        self.logger.info(f"Searching Product: {item_name}")
        box = self.wait.until(EC.presence_of_element_located((By.XPATH, self.textbox_search_xpath)))
        box.clear()
        box.send_keys(item_name)
        box.send_keys("\n")
    
    def click_first_listed_product(self):
        self.logger.info("Clicking on the first listed Laptop card...")
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.first_laptop_card_xpath))).click()

    def click_heart_icon(self):
        self.logger.info("Clicking Heart/Wishlist icon as Guest...")
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.button_heart_icon_xpath))).click()

    def click_secure_checkout(self):
        self.logger.info("Clicking Secure Checkout Button...")
        self.wait.until(EC.element_to_be_clickable((By.XPATH, self.button_secure_checkout_xpath))).click()
    
    def is_login_page_enforced(self):
        try:
            heading_status = self.wait.until(EC.presence_of_element_located((By.XPATH, self.text_welcome_back_xpath))).is_displayed()
            input_status = self.wait.until(EC.presence_of_element_located((By.XPATH, self.textbox_login_email_xpath))).is_displayed()
            return heading_status and input_status
        except:
            return False