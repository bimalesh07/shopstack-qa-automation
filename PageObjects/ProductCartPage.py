
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Utilities.customLogger import LogGen
import time
from selenium.common.exceptions import StaleElementReferenceException

class ProductCartPage:
    # NAVBAR SHOP LINK & INITIAL LOADING SPINNER
    button_shop_nav_xpath = "//a[normalize-space()='Shop']"
    loading_spinner_xpath = "//*[contains(text(), 'Curating best products for you')]"
    
    # REACTIVE FILTERS & SORTING CONTROLLERS (Super Robust Dynamic Locator combo)
    button_filters_toggle_xpath = (
        "//button[contains(., 'Filter') or contains(., 'FILTER')]"
        " | //span[contains(., 'Filter') or contains(., 'FILTER')]"
        " | //*[contains(@class, 'filter') and @type='button']"
    )
    textbox_min_price_xpath = "//input[@placeholder='Min']"
    textbox_max_price_xpath = "//input[@placeholder='Max']"
    button_reset_filters_xpath = "//button[normalize-space()='Reset All Filters']"
    
    # Custom Dropdown Sorting Locators
    button_sort_dropdown_xpath = "//select[contains(., 'NEWEST FIRST') or contains(., 'Newest First')]"
    option_low_to_high_xpath = "//select/option[@value='price']"
    option_high_to_low_xpath = "//select/option[@value='-price']"
    option_newest_first_xpath = "//select/option[@value='-created_at']"
    option_oldest_first_xpath = "//select/option[@value='created_at']"

    # WISHLIST TARGET MATRIX
    button_wishlist_heart_xpath = "(//div[contains(@class, 'grid')]//button[contains(@class, 'hover:text-red-500')])[1]"
    text_wishlist_toast_xpath ="//*[contains(text(), 'Added to wishlist!') or contains(text(), 'ADDED TO WISHLIST')]"

    # PRODUCT CARD SELECTION & DETAILS LANDMARK PROOF 
    first_product_card_xpath = "//div[@class='grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6']//a[1]"
    button_secure_checkout_xpath = "//span[normalize-space()='Secure Checkout'] | //button[contains(., 'Checkout')]"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 15)
        self.logger = LogGen.loggen()

    def navigate_to_shop_page(self):
        self.logger.info("👉 Force-Clicking NAVBAR SHOP link using JavaScript Pipeline...")
        shop_nav = self.wait.until(EC.presence_of_element_located((By.XPATH, self.button_shop_nav_xpath) if hasattr(By, '滿足') else (By.XPATH, self.button_shop_nav_xpath)))
        self.driver.execute_script("arguments[0].click();", shop_nav)
        
        try:
            WebDriverWait(self.driver, 9).until(
                EC.invisibility_of_element_located((By.XPATH, self.loading_spinner_xpath))
            )
            self.logger.info("Loader gone! Shop items are now visible on screen.")
        except:
            self.logger.warning("Loader sync timeout or page loaded instantly.")
    
    def apply_reactive_price_filters(self, min_price, max_price):
        self.logger.info("Giving 4 seconds for initial shop layout stabilization...")
        time.sleep(4)
        
        self.logger.info("🔍 Expanding Filters panel using Master Combo Xpath...")
        filters_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, self.button_filters_toggle_xpath)))

        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", filters_btn)
        time.sleep(1)
        self.driver.execute_script("arguments[0].click();", filters_btn)
        self.logger.info("Filters panel toggle clicked successfully.")
        time.sleep(2.5) 

        #INPUT MIN PRICE
        min_field = self.wait.until(EC.presence_of_element_located((By.XPATH, self.textbox_min_price_xpath)))
        min_field.clear()
        min_field.send_keys(min_price)
        self.logger.info(f"Min Price set to: {min_price}")

        #WAITING FOR LOADER TO SYNC & CLEAR
        self.logger.info("Min input completed. Waiting for dynamic reactive loader to sync and clear...")
        time.sleep(1.5) 
        
        try:
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located((By.XPATH, self.loading_spinner_xpath))
            )
            self.logger.info("Reactive page filter update loader disappeared safely.")
        except:
            self.logger.warning("Reactive loader didn't appear or cleared out instantly.")

        # Post-loader wait to allow layout to load completely
        self.logger.info("⏳ Giving 3 seconds breathing buffer for DOM initialization post-refresh...")
        time.sleep(3)

        #INPUT MAX PRICE (With Stale-Element Exception Proof Loop )
        self.logger.info("🔍 Entering Stale-Proof Input Loop for Max Price Field...")
        
        for attempt in range(1, 4): # Retry 3 times if stale element exception occurs
            try:
                self.logger.info(f" Max Field Entry Attempt {attempt}/3...")
                
                # Fresh re-catch inside loop
                max_field = self.wait.until(EC.presence_of_element_located((By.XPATH, self.textbox_max_price_xpath)))
                
                # JavaScript clearing and focusing
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", max_field)
                self.driver.execute_script("arguments[0].click();", max_field)
                max_field.clear()
                
                # Type the price
                max_field.send_keys(max_price)
                self.logger.info(f"📥 Success: Max Price strictly set to: {max_price}")
                break # Exit loop if input is successful
                
            except Exception as e:
                self.logger.warning(f" Attempt {attempt} intercepted by Stale reference or UI block. Retrying in 1.5s...")
                time.sleep(1.5)
        else:
            # If it fails after 3 attempts, raise exception
            raise StaleElementReferenceException("Critical Block: Max Price element is continuously unstable.")
        
        time.sleep(4) # Wait for complete filtered dataset array refresh

      

    def apply_sorting_filter(self, choice):
        self.logger.info(f"🎯 Attempting UI interaction on sorting element for choice: {choice}")
        dropdown_head = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.button_sort_dropdown_xpath)))
        self.driver.execute_script("arguments[0].click();", dropdown_head)
        self.logger.info("Main dropdown element clicked and options list expanded.")
        time.sleep(1)

        if choice.lower() == "low to high":
            target_xpath = self.option_low_to_high_xpath
            self.logger.info("Target Option Set: PRICE: LOW TO HIGH")
        elif choice.lower() == "high to low":
            target_xpath = self.option_high_to_low_xpath
            self.logger.info("Target Option Set: PRICE: HIGH TO LOW")
        elif choice.lower() == "newest":
            target_xpath = self.option_newest_first_xpath
            self.logger.info("Target Option Set: NEWEST FIRST")
        elif choice.lower() == "oldest":
            target_xpath = self.option_oldest_first_xpath
            self.logger.info("Target Option Set: OLDEST FIRST")
        else:
            raise ValueError(f"Invalid sorting choice string dispatched: {choice}")

        target_option_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, target_xpath)))
        self.driver.execute_script("arguments[0].click();", target_option_element)
        
        self.logger.info(f"🎉 Success: Selected option node parameter updated to state: {choice}")
        time.sleep(3)
        
    def click_wishlist_heart_and_capture_toast(self):
        self.logger.info("Clicking Wishlist Heart button...")
        heart_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.button_wishlist_heart_xpath)))
        
        # Fix: Try standard click first
        # This is safe if there is no UI overlay issue.
        try:
            heart_btn.click()
        except:
            # Fallback: If normal click is blocked, run Javascript click
            self.driver.execute_script("arguments[0].click();", heart_btn)
        """
        If multiple paths exist, target the first element
        # find_elements returns a list of all matching buttons
        heart_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@class, 'hover:text-red-500')]")
        
        if len(heart_buttons) > 0:
            # Use index [0] to get the first button and click via JavaScript to avoid JavascriptException
            self.driver.execute_script("arguments[0].click();", heart_buttons[0])
        else:
            self.logger.error("No heart buttons found!")
            return ""
        
        """
        try:
            toast_bubble = WebDriverWait(self.driver, 6).until(
                EC.visibility_of_element_located((By.XPATH, self.text_wishlist_toast_xpath))
            )
            time.sleep(1.5)

            capture_msg = toast_bubble.text
            return capture_msg 
        except:
            self.logger.error("Failed to catch the wishlist success toast.")
            return ""
    
    def click_product_to_open_details(self):
        self.logger.info("Clicking the product card to step into details view model...")
        product_card = self.wait.until(EC.element_to_be_clickable((By.XPATH, self.first_product_card_xpath)))
        self.driver.execute_script("arguments[0].click();", product_card)
        time.sleep(3)

    def is_details_page_opened_successfully(self):
        try:
            current_url = self.driver.current_url.lower()
            checkout_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, self.button_secure_checkout_xpath)))
            
            if "product" in current_url and checkout_btn.is_displayed():
                return True
            return False
        except:
            return False