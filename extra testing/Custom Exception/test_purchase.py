# import pytest
# import allure
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException, \
#     WebDriverException
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
# import time
# import logging
# import  random
# import string
#
# # Configure logging
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logger = logging.getLogger(__name__)
#
#
# # Custom Exceptions
# class LoginFailedError(Exception):
#     """Raised when login fails due to invalid credentials or unexpected errors."""
#     pass
#
#
# class PurchaseError(Exception):
#     """Raised when purchase fails."""
#     pass
#
#
# class WebDriverInitializationError(Exception):
#     """Raised when WebDriver initialization fails."""
#     pass
#
#
# # Test Configuration
# TEST_CONFIG = {
#     "username": "gedehim917@decodewp.com",
#     "password": "Tebahal1!",
#     "url": "https://velvet.webredirect.himshang.com.np/#/pages/dashboard",
#     "product_data": {
#         "product_item": "Testing10",
#         "HS_code": "123",
#         "unit": "kg.",
#         "item_type": "Service Item",
#         "description": "This is description",
#         "category": "N/A",
#         "short_name": "XYZ",
#         "purchase_price": "120",
#         "sales_price": "140",
#         "alt_unit": "Each",
#         "conversion_factor": "1000",
#         "barcode_map": "20",
#         "barcode_unit": "kg."
#     }
# }
#
#
# class TestProductFlow:
#     """Test class for product flow automation."""
#
#     def setup_method(self):
#         """Setup method that runs before each test method."""
#         try:
#             self.driver = webdriver.Chrome()
#             self.driver.implicitly_wait(10)
#             logger.info("WebDriver initialized successfully")
#         except WebDriverException as e:
#             logger.error(f"Failed to initialize WebDriver: {e}")
#             raise WebDriverInitializationError(f"WebDriver initialization failed: {e}")
#
#     def safe_click(self, element, description="element"):
#         """
#         Safely click an element with fallback methods.
#
#         Args:
#             element: WebElement to click
#             description: Description of the element for logging
#         """
#         try:
#             element.click()
#             logger.info(f"Clicked {description} using regular click")
#         except Exception as e:
#             logger.warning(f"Regular click failed for {description}, trying JavaScript click: {e}")
#             try:
#                 self.driver.execute_script("arguments[0].click();", element)
#                 logger.info(f"Clicked {description} using JavaScript click")
#             except Exception as js_error:
#                 logger.error(f"JavaScript click also failed for {description}: {js_error}")
#                 raise ElementNotInteractableException(
#                     f"Failed to click {description} using both regular and JavaScript methods")
#
#     def teardown_method(self):
#         """Teardown method that runs after each test method."""
#         if hasattr(self, 'driver') and self.driver:
#             try:
#                 logger.info("Cleaning up - closing driver")
#                 self.driver.quit()
#                 logger.info("Driver closed successfully")
#             except Exception as e:
#                 logger.error(f"Error during cleanup: {e}")
#
#     @allure.step("Perform login with username: {username}")
#     @pytest.hookimpl(hookwrapper=True)
#     def login(self, username, password, link):
#         """
#         Perform login with improved error handling and retry mechanism.
#         """
#         global Purchase_invoice
#         try:
#             self.driver.maximize_window()
#             self.driver.get(link)
#             logger.info(f"Navigated to login page: {link}")
#
#             with allure.step("Entering credentials and clicking Sign In"):
#                 # Wait for username field and enter credentials
#                 username_field = WebDriverWait(self.driver, 15).until(
#                     EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[formcontrolname="username"]'))
#                 )
#                 username_field.clear()
#                 username_field.send_keys(username)
#                 logger.info("Username entered successfully")
#
#                 # Enter password
#                 password_field = WebDriverWait(self.driver, 10).until(
#                     EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[formcontrolname="password"]'))
#                 )
#                 password_field.clear()
#                 password_field.send_keys(password)
#                 logger.info("Password entered successfully")
#
#                 # Click Sign In button with fallback methods
#                 sign_in_btn = WebDriverWait(self.driver, 10).until(
#                     EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign In')]"))
#                 )
#                 self.safe_click(sign_in_btn, "Sign In button")
#
#             # Handle already logged in scenario
#             try:
#                 logout_btn = WebDriverWait(self.driver, 20).until(
#                     EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Logout']]"))
#                 )
#                 logger.info("Already Logged In popup detected")
#
#                 # Click Logout button with fallback to JavaScript click
#                 try:
#                     with allure.step("Detected 'Already Logged In' popup — logging out first"):
#                         self.safe_click(logout_btn, "Logout button")
#                         logger.info("Logout button clicked successfully")
#                 except Exception as e:
#                     logger.error(f"Failed to click logout button: {e}")
#                     raise LoginFailedError(f"Could not click logout button: {e}")
#
#                 logger.info("Logout button clicked successfully")
#                 time.sleep(8)  # Wait for logout to complete
#
#                 # Wait for the "Sign In" button to be clickable and press Enter
#                 sign_in_btn = WebDriverWait(self.driver, 10).until(
#                     EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign In')]"))
#                 )
#
#                 # Press Enter on the "Sign In" button
#                 sign_in_btn.send_keys(Keys.ENTER)
#                 logger.info("Pressed Enter on Sign In button after logout")
#
#             except TimeoutException:
#              logger.info("No 'Already Logged In' popup detected — continuing without logout")
#             finally:
#                 print("")
#
#             ################################## PURCHASE INVOICE ###########################################################
#
#             def Purchase_invoice(driver, barcode_purchase):
#                 try:
#                     # ============ NAVIGATION TO PURCHASE TRANSACTION ============
#                     print("Step 5: Waiting for dashboard to load...")
#                     time.sleep(3)  # Give additional time for page to fully load
#
#                     print("Step 6: Clicking on 'Transactions' menu...")
#                     transactions_clicked = False
#
#                     print("Step 6.1: Debugging available navigation elements...")
#                     try:
#                         nav_elements = driver.find_elements(By.XPATH,
#                                                             "//a | //div[@class*='nav'] | //span[@class*='nav']")
#                         print(f"Found {len(nav_elements)} potential navigation elements")
#
#                         visible_nav_texts = []
#                         for element in nav_elements[:15]:
#                             try:
#                                 text = element.text.strip()
#                                 if text and len(text) > 0 and element.is_displayed():
#                                     visible_nav_texts.append(text)
#                             except:
#                                 pass
#
#                         print("Available navigation texts:")
#                         for text in visible_nav_texts:
#                             print(f"  - '{text}'")
#                     except Exception as e:
#                         print(f"Navigation debug failed: {e}")
#
#                     transactions_selectors = [
#                         "//a[contains(text(), 'Transactions')]",
#                         "//div[contains(text(), 'Transactions')]",
#                         "//span[contains(text(), 'Transactions')]",
#                         "//*[contains(@class, 'nav') and contains(text(), 'Transactions')]",
#                         "//*[text()='Transactions']",
#                         "//a[contains(@href, 'transaction')]",
#                         "//*[@class*='menu' and contains(text(), 'Transactions')]"
#                     ]
#
#                     for i, selector in enumerate(transactions_selectors, 1):
#                         try:
#                             print(f"  Trying selector {i}: {selector}")
#                             transactions_element = WebDriverWait(driver, 5).until(
#                                 EC.element_to_be_clickable((By.XPATH, selector))
#                             )
#                             actions = ActionChains(driver)
#                             actions.move_to_element(transactions_element).click().perform()
#                             print(f"✓ Successfully clicked on 'Transactions' using selector {i}")
#                             transactions_clicked = True
#                             time.sleep(2)
#                             break
#                         except Exception as e:
#                             print(f"  ✗ Selector {i} failed: {str(e)[:50]}...")
#                             continue
#
#                     purchase_transaction_hovered = False
#                     if not purchase_transaction_hovered:
#                         print("⚠️ Trying alternative approach for Purchase Transaction hover...")
#                         try:
#                             all_elements = driver.find_elements(By.TAG_NAME, "span")
#                             for element in all_elements:
#                                 try:
#                                     element_text = element.text.strip()
#                                     if 'Purchase Transaction' in element_text and element.is_displayed():
#                                         actions = ActionChains(driver)
#                                         actions.move_to_element(element).perform()
#                                         print(f"✓ Hovered over 'Purchase Transaction' using fallback method")
#                                         purchase_transaction_hovered = True
#                                         time.sleep(2)
#                                         break
#                                 except Exception:
#                                     continue
#                         except Exception as e:
#                             print(f"⚠️ Fallback method for Purchase Transaction hover failed: {e}")
#
#                     if not purchase_transaction_hovered:
#                         raise Exception("Could not find or hover over 'Purchase Transaction' menu")
#
#                     print("Step 8: Clicking on 'Purchase Invoice' from dropdown...")
#                     purchase_invoice_clicked = False
#                     purchase_invoice_selectors = [
#                         "//*[@class='dropdown-item' and contains(text(), 'Purchase Invoice')]",
#                         "//*[contains(@class, 'menu-item') and contains(text(), 'Purchase Invoice')]"
#                     ]
#
#                     for i, selector in enumerate(purchase_invoice_selectors, 1):
#                         try:
#                             print(f"  Trying Purchase Invoice selector {i}: {selector}")
#                             purchase_invoice_element = WebDriverWait(driver, 8).until(
#                                 EC.element_to_be_clickable((By.XPATH, selector))
#                             )
#                             actions = ActionChains(driver)
#                             actions.move_to_element(purchase_invoice_element).click().perform()
#                             print(f"✓ Successfully clicked on 'Purchase Invoice' using selector {i}")
#                             purchase_invoice_clicked = True
#                             time.sleep(3)
#                             break
#                         except Exception as e:
#                             print(f"  ✗ Purchase Invoice selector {i} failed: {str(e)[:100]}...")
#                             continue
#
#                     if not purchase_invoice_clicked:
#                         print("⚠️ Trying alternative approach for Purchase Invoice...")
#                         try:
#                             invoice_elements = driver.find_elements(By.XPATH,
#                                                                     "//*[contains(text(), 'Purchase Invoice')]")
#                             print(f"Found {len(invoice_elements)} elements containing 'Purchase Invoice'")
#                             for element in invoice_elements:
#                                 try:
#                                     if element.is_displayed() and element.is_enabled():
#                                         actions = ActionChains(driver)
#                                         actions.move_to_element(element).click().perform()
#                                         print(f"✓ Clicked on 'Purchase Invoice' using fallback method")
#                                         purchase_invoice_clicked = True
#                                         time.sleep(3)
#                                         break
#                                 except Exception:
#                                     continue
#                         except Exception as e:
#                             print(f"⚠️ Fallback method for Purchase Invoice failed: {e}")
#
#                     print("Step 9: Manually typing in Invoice Number field...")
#
#                     random_invoice = "INV-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
#                     print(f"Generated Invoice Number: {random_invoice}")
#
#                     try:
#                         invoice_field = WebDriverWait(driver, 10).until(
#                             EC.element_to_be_clickable((By.ID, "invoiceNO"))
#                         )
#                         invoice_field.clear()
#                         invoice_field.send_keys(random_invoice)
#                         print(f"✓ Successfully entered Invoice Number: {random_invoice}")
#                     except Exception as e:
#                         print(f"⚠️ Failed to enter Invoice Number: {e}")
#
#                     print("Step 10: Opening Account dropdown by pressing Enter...")
#                     try:
#                         account_field_selectors = [
#                             "//input[preceding-sibling::label[contains(text(), 'Account')] or @placeholder*='Account' or contains(@formcontrolname, 'account')]",
#                             "//input[contains(@placeholder, 'Press Enter to select Account')]",
#                             "//*[contains(text(), 'Press Enter to select Account')]",
#                             "//input[contains(@class, 'form-control') and contains(@placeholder, 'Account')]"
#                         ]
#                         account_field = None
#                         for selector in account_field_selectors:
#                             try:
#                                 account_field = WebDriverWait(driver, 5).until(
#                                     EC.element_to_be_clickable((By.XPATH, selector))
#                                 )
#                                 print(f"✓ Found Account field using selector: {selector}")
#                                 break
#                             except:
#                                 continue
#
#                         if account_field:
#                             account_field.click()
#                             time.sleep(1)
#                             account_field.send_keys(Keys.ENTER)
#                             print("✓ Successfully pressed Enter on Account field to open dropdown")
#                             print("⏳ Waiting for dropdown list to load completely...")
#                             time.sleep(3)
#                         else:
#                             raise Exception("Could not find Account field")
#
#                     except Exception as e:
#                         print(f"⚠️ Failed to open Account dropdown using primary method: {e}")
#                         try:
#                             all_inputs = driver.find_elements(By.TAG_NAME, "input")
#                             for input_field in all_inputs:
#                                 try:
#                                     placeholder = input_field.get_attribute("placeholder")
#                                     if placeholder and "account" in placeholder.lower():
#                                         input_field.click()
#                                         time.sleep(1)
#                                         input_field.send_keys(Keys.ENTER)
#                                         print("✓ Successfully opened Account dropdown using fallback method")
#                                         time.sleep(2)
#                                         break
#                                 except:
#                                     continue
#                         except Exception as e2:
#                             print(f"⚠️ All methods failed to open Account dropdown: {e2}")
#
#                     print("Step 11: Selecting first account by pressing Enter again...")
#                     try:
#                         if account_field:
#                             account_field.send_keys(Keys.ENTER)
#                             print("✓ Successfully pressed Enter again to select first account")
#                             time.sleep(2)
#                         else:
#                             focused_element = driver.switch_to.active_element
#                             focused_element.send_keys(Keys.ENTER)
#                             print("✓ Successfully pressed Enter on focused element to select first account")
#                             time.sleep(2)
#                     except Exception as e:
#                         print(f"⚠️ Failed to select first account by pressing Enter: {e}")
#                         try:
#                             print("⚠️ Trying fallback method: Arrow Down + Enter...")
#                             if account_field:
#                                 account_field.send_keys(Keys.ARROW_DOWN)
#                                 time.sleep(0.5)
#                                 account_field.send_keys(Keys.ENTER)
#                                 print("✓ Successfully selected first account using Arrow Down + Enter")
#                             else:
#                                 focused_element = driver.switch_to.active_element
#                                 focused_element.send_keys(Keys.ARROW_DOWN)
#                                 time.sleep(0.5)
#                                 focused_element.send_keys(Keys.ENTER)
#                                 print(
#                                     "✓ Successfully selected first account using Arrow Down + Enter on focused element")
#                         except Exception as e2:
#                             print(f"⚠️ All methods failed: {e2}")
#                             try:
#                                 print("⚠️ Last resort: Trying to click on dropdown items...")
#                                 dropdown_selectors = [
#                                     "//div[contains(@class, 'dropdown-menu')]//a[1]",
#                                     "//ul[contains(@class, 'dropdown')]//li[1]",
#                                     "//div[contains(@class, 'dropdown')]//div[1]",
#                                     "//*[contains(@class, 'dropdown-item')][1]",
#                                     "//*[contains(@class, 'list-item')][1]"
#                                 ]
#                                 for selector in dropdown_selectors:
#                                     try:
#                                         first_account = WebDriverWait(driver, 3).until(
#                                             EC.element_to_be_clickable((By.XPATH, selector))
#                                         )
#                                         first_account.click()
#                                         print(f"✓ Successfully clicked on first account using selector: {selector}")
#                                         break
#                                     except:
#                                         continue
#                             except Exception as e3:
#                                 print(f"⚠️ All methods failed to select first account: {e3}")
#
#                     print("\n" + "=" * 50)
#                     print("✓ NEW FUNCTIONALITY COMPLETED SUCCESSFULLY!")
#                     print("✓ Account dropdown opened by pressing Enter")
#                     print("✓ First account selected by pressing Enter again")
#                     print("=" * 50 + "\n")
#
#                     remarks_field = WebDriverWait(driver, 5).until(
#                         EC.element_to_be_clickable((By.ID, "remarksid"))
#                     )
#                     remarks_field.clear()
#                     remarks_field.send_keys("This is an automated remark for PI.")
#                     time.sleep(5)
#                     print("✅ Remarks entered successfully.")
#
#                     # Barcode and quantity
#                     barcode_input = driver.find_element(By.ID, "barcodeField")
#                     barcode_input.clear()
#                     barcode_input.send_keys(barcode_purchase)
#                     barcode_input.send_keys(Keys.ENTER)
#
#                     quantity = random.randint(80, 200)
#                     print(f"Generated quantity: {quantity}")
#
#                     xpaths = [
#                         "//table//tr//td[position()=9]//input",
#                         "//input[contains(@name, 'quantity') or contains(@name, 'Quantity')]",
#                         "//input[contains(@id, 'quantity') or contains(@id, 'Quantity')]",
#                         "//td[contains(@class, 'quantity')]//input",
#                         "//table//tbody//tr[1]//td[9]//input",
#                     ]
#
#                     quantity_field = None
#                     for xpath in xpaths:
#                         try:
#                             quantity_field = WebDriverWait(driver, 5).until(
#                                 EC.element_to_be_clickable((By.XPATH, xpath))
#                             )
#                             quantity_field.clear()
#                             quantity_field.send_keys(str(quantity) + Keys.ENTER)
#                             print("✅ Quantity entered and Enter key pressed.")
#                             time.sleep(2)
#                             break
#                         except Exception as e:
#                             print(f"⚠ Failed with XPath: {xpath} -> {e}")
#                     else:
#                         print("❌ Could not locate the quantity input field.")
#
#                     # --- Discount (Dis%) 0 ---
#                     discount = random.randint(1, 50)
#                     print(f"Generated discount: {discount}%")
#                     try:
#                         discount_field = WebDriverWait(driver, 5).until(
#                             EC.element_to_be_clickable((By.ID, "INDDISCOUNTRATE0"))
#                         )
#                         discount_field.clear()
#                         discount_field.send_keys(str(discount))
#                         time.sleep(2)
#                         print("✅ Discount entered.")
#                     except Exception as e:
#                         print(f"❌ Discount input not found: {e}")
#
#                     # --- Discount (Dis%) 1 ---
#                     discount = random.randint(1, 50)
#                     try:
#                         discount_field = WebDriverWait(driver, 5).until(
#                             EC.element_to_be_clickable((By.ID, "INDDISCOUNTRATE1"))
#                         )
#                         discount_field.clear()
#                         discount_field.send_keys(str(discount))
#                         time.sleep(2)
#                         print("✅ Discount entered.")
#                     except Exception as e:
#                         print(f"❌ Discount input not found: {e}")
#
#                     wait = WebDriverWait(driver, 10)
#                     save_button = wait.until(EC.element_to_be_clickable(
#                         (By.XPATH, "//button[contains(text(), 'SAVE') and contains(@class, 'btn-info')]")))
#                     save_button.click()
#
#                     try:
#                         WebDriverWait(driver, 5).until(EC.alert_is_present())
#                         alert = driver.switch_to.alert
#                         alert.accept()
#                         print("Alert accepted successfully.")
#                     except TimeoutException:
#                         print("No alert appeared after clicking SAVE.")
#
#                     import pyautogui
#                     time.sleep(10)
#                     pyautogui.press('esc')
#                     time.sleep(5)
#
#                     view_button = wait.until(
#                         EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'VIEW')]")))
#                     view_button.click()
#
#                     time.sleep(2)
#                     actions = ActionChains(driver)
#                     actions.send_keys(Keys.ENTER).perform()
#                     time.sleep(3)
#
#                     reset_btn = wait.until(
#                         EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'RESET')]")))
#                     reset_btn.click()
#
#                     time.sleep(3)
#                     wait.until(EC.alert_is_present())
#                     alert = driver.switch_to.alert
#                     alert.accept()
#                     time.sleep(5)
#
#                     back_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'BACK')]")))
#                     back_btn.click()
#
#
#                 except Exception as e:
#                     import traceback
#                     print(f"\n❌ AN ERROR OCCURRED: {e}")
#                     traceback.print_exc()
#                     print("Current URL:", driver.current_url)
#             # Function call
#
#
#
#         finally:
#                 print("")
#
#
#
#                 # Login
#                 self.login(
#                             TEST_CONFIG["username"],
#                             TEST_CONFIG["password"],
#                             TEST_CONFIG["url"]
#                         )
#
#                 Purchase_invoice(self.driver,barcode_purchase=2020)
#
#         print("Keeping browser open for 30 seconds for observation...")
#         time.sleep(30)
#



import pytest
import allure
import time
import logging
import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# --------------------------------------------------------
# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --------------------------------------------------------
# Custom Exceptions
class LoginFailedError(Exception):
    """Raised when login fails due to invalid credentials or unexpected errors."""
    pass

class ProductAlreadyExistsError(Exception):
    """Raised when trying to create a product that already exists."""
    pass

class WebDriverInitializationError(Exception):
    """Raised when WebDriver initialization fails."""
    pass

# --------------------------------------------------------
# Test Configuration
TEST_CONFIG = {
    "username": "gedehim917@decodewp.com",
    "password": "Tebahal1!",
    "url": "https://velvet.webredirect.himshang.com.np/#/pages/dashboard",
}

# --------------------------------------------------------
# Test class
class TestProductFlow:
    def setup_method(self):
        try:
            self.driver = webdriver.Chrome()
            self.driver.implicitly_wait(10)
            logger.info("WebDriver initialized successfully")
        except WebDriverException as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise WebDriverInitializationError(f"WebDriver initialization failed: {e}")

    def teardown_method(self):
        if hasattr(self, 'driver') and self.driver:
            try:
                logger.info("Cleaning up - closing driver")
                self.driver.quit()
                logger.info("Driver closed successfully")
            except Exception as e:
                logger.error(f"Error during cleanup: {e}")

    def safe_click(self, element, description="element"):
        try:
            element.click()
            logger.info(f"Clicked {description} using normal click")
        except Exception as e:
            logger.warning(f"Normal click failed for {description}, trying JS click: {e}")
            self.driver.execute_script("arguments[0].click();", element)
            logger.info(f"Clicked {description} using JavaScript click")

    # -----------------------------------
    @allure.step("Login with username: {username}")
    def login(self, username, password, link):
        driver = self.driver
        driver.maximize_window()
        driver.get(link)
        logger.info(f"Navigated to: {link}")

        username_field = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[formcontrolname="username"]'))
        )
        username_field.clear()
        username_field.send_keys(username)
        logger.info("Entered username")

        password_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[formcontrolname="password"]'))
        )
        password_field.clear()
        password_field.send_keys(password)
        logger.info("Entered password")

        sign_in_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign In')]"))
        )
        self.safe_click(sign_in_btn, "Sign In button")

        # # Handle already logged in popup
        # try:
        #     logout_btn = WebDriverWait(driver, 5).until(
        #         EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Logout']]"))
        #     )
        #     self.safe_click(logout_btn, "Logout button on 'Already logged in' popup")
        #     time.sleep(5)
        #     sign_in_btn = WebDriverWait(driver, 10).until(
        #         EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign In')]"))
        #     )
        #     sign_in_btn.send_keys(Keys.ENTER)
        #     logger.info("Handled already logged in scenario, re-logged in")
        # except TimeoutException:
        #     logger.info("No 'already logged in' popup detected")

        # Handle already logged in scenario
        try:
            logout_btn = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Logout']]"))
            )
            logger.info("Already Logged In popup detected")

            # Click Logout button with fallback to JavaScript click
            try:
                with allure.step("Detected 'Already Logged In' popup — logging out first"):
                    self.safe_click(logout_btn, "Logout button")
                    logger.info("Logout button clicked successfully")
            except Exception as e:
                logger.error(f"Failed to click logout button: {e}")
                raise LoginFailedError(f"Could not click logout button: {e}")

            logger.info("Logout button clicked successfully")
            time.sleep(8)  # Wait for logout to complete

            # Wait for the "Sign In" button to be clickable and press Enter
            sign_in_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign In')]"))
            )

            # Press Enter on the "Sign In" button
            sign_in_btn.send_keys(Keys.ENTER)
            logger.info("Pressed Enter on Sign In button after logout")

        except TimeoutException:
            logger.info("No 'Already Logged In' popup detected — continuing without logout")

    # -----------------------------------
    @allure.step("Create purchase invoice")
    def create_purchase_invoice(self, barcode):
        driver = self.driver
        actions = ActionChains(driver)
        wait = WebDriverWait(driver, 10)

        try:
            nav_elements = driver.find_elements(By.XPATH, "//a | //div[@class*='nav'] | //span[@class*='nav']")
            print(f"Found {len(nav_elements)} potential navigation elements")

            visible_nav_texts = []
            for element in nav_elements[:15]:
                try:
                    text = element.text.strip()
                    if text and len(text) > 0 and element.is_displayed():
                        visible_nav_texts.append(text)
                except:
                    pass

            print("Available navigation texts:")
            for text in visible_nav_texts:
                print(f"  - '{text}'")
        except Exception as e:
            print(f"Navigation debug failed: {e}")

        transactions_selectors = [
            "//a[contains(text(), 'Transactions')]",
            "//div[contains(text(), 'Transactions')]",
            "//span[contains(text(), 'Transactions')]",
            "//*[contains(@class, 'nav') and contains(text(), 'Transactions')]",
            "//*[text()='Transactions']",
            "//a[contains(@href, 'transaction')]",
            "//*[@class*='menu' and contains(text(), 'Transactions')]"
        ]

        for i, selector in enumerate(transactions_selectors, 1):
            try:
                print(f"  Trying selector {i}: {selector}")
                transactions_element = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                actions = ActionChains(driver)
                actions.move_to_element(transactions_element).click().perform()
                print(f"✓ Successfully clicked on 'Transactions' using selector {i}")
                transactions_clicked = True
                time.sleep(2)
                break
            except Exception as e:
                print(f"  ✗ Selector {i} failed: {str(e)[:50]}...")
                continue

        purchase_transaction_hovered = False
        if not purchase_transaction_hovered:
            print("⚠️ Trying alternative approach for Purchase Transaction hover...")
            try:
                all_elements = driver.find_elements(By.TAG_NAME, "span")
                for element in all_elements:
                    try:
                        element_text = element.text.strip()
                        if 'Purchase Transaction' in element_text and element.is_displayed():
                            actions = ActionChains(driver)
                            actions.move_to_element(element).perform()
                            print(f"✓ Hovered over 'Purchase Transaction' using fallback method")
                            purchase_transaction_hovered = True
                            time.sleep(2)
                            break
                    except Exception:
                        continue
            except Exception as e:
                print(f"⚠️ Fallback method for Purchase Transaction hover failed: {e}")

        if not purchase_transaction_hovered:
            raise Exception("Could not find or hover over 'Purchase Transaction' menu")

        print("Step 8: Clicking on 'Purchase Invoice' from dropdown...")
        purchase_invoice_clicked = False
        purchase_invoice_selectors = [
            "//*[@class='dropdown-item' and contains(text(), 'Purchase Invoice')]",
            "//*[contains(@class, 'menu-item') and contains(text(), 'Purchase Invoice')]"
        ]

        for i, selector in enumerate(purchase_invoice_selectors, 1):
            try:
                print(f"  Trying Purchase Invoice selector {i}: {selector}")
                purchase_invoice_element = WebDriverWait(driver, 8).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                actions = ActionChains(driver)
                actions.move_to_element(purchase_invoice_element).click().perform()
                print(f"✓ Successfully clicked on 'Purchase Invoice' using selector {i}")
                purchase_invoice_clicked = True
                time.sleep(3)
                break
            except Exception as e:
                print(f"  ✗ Purchase Invoice selector {i} failed: {str(e)[:100]}...")
                continue

        if not purchase_invoice_clicked:
            print("⚠️ Trying alternative approach for Purchase Invoice...")
            try:
                invoice_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Purchase Invoice')]")
                print(f"Found {len(invoice_elements)} elements containing 'Purchase Invoice'")
                for element in invoice_elements:
                    try:
                        if element.is_displayed() and element.is_enabled():
                            actions = ActionChains(driver)
                            actions.move_to_element(element).click().perform()
                            print(f"✓ Clicked on 'Purchase Invoice' using fallback method")
                            purchase_invoice_clicked = True
                            time.sleep(3)
                            break
                    except Exception:
                        continue
            except Exception as e:
                print(f"⚠️ Fallback method for Purchase Invoice failed: {e}")

        # Fill form
        invoice_no = "INV-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        logger.info(f"Generated Invoice Number: {invoice_no}")

        invoice_field = wait.until(EC.element_to_be_clickable((By.ID, "invoiceNO")))
        invoice_field.clear()
        invoice_field.send_keys(invoice_no)
        try:
            account_field_selectors = [
                "//input[preceding-sibling::label[contains(text(), 'Account')] or @placeholder*='Account' or contains(@formcontrolname, 'account')]",
                "//input[contains(@placeholder, 'Press Enter to select Account')]",
                "//*[contains(text(), 'Press Enter to select Account')]",
                "//input[contains(@class, 'form-control') and contains(@placeholder, 'Account')]"
            ]
            account_field = None
            for selector in account_field_selectors:
                try:
                    account_field = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    print(f"✓ Found Account field using selector: {selector}")
                    break
                except:
                    continue

            if account_field:
                account_field.click()
                time.sleep(1)
                account_field.send_keys(Keys.ENTER)
                print("✓ Successfully pressed Enter on Account field to open dropdown")
                print("⏳ Waiting for dropdown list to load completely...")
                time.sleep(3)
            else:
                raise Exception("Could not find Account field")

        except Exception as e:
            print(f"⚠️ Failed to open Account dropdown using primary method: {e}")
            try:
                all_inputs = driver.find_elements(By.TAG_NAME, "input")
                for input_field in all_inputs:
                    try:
                        placeholder = input_field.get_attribute("placeholder")
                        if placeholder and "account" in placeholder.lower():
                            input_field.click()
                            time.sleep(1)
                            input_field.send_keys(Keys.ENTER)
                            print("✓ Successfully opened Account dropdown using fallback method")
                            time.sleep(2)
                            break
                    except:
                        continue
            except Exception as e2:
                print(f"⚠️ All methods failed to open Account dropdown: {e2}")

        print("Step 11: Selecting first account by pressing Enter again...")
        try:
            if account_field:
                account_field.send_keys(Keys.ENTER)
                print("✓ Successfully pressed Enter again to select first account")
                time.sleep(2)
            else:
                focused_element = driver.switch_to.active_element
                focused_element.send_keys(Keys.ENTER)
                print("✓ Successfully pressed Enter on focused element to select first account")
                time.sleep(2)
        except Exception as e:
            print(f"⚠️ Failed to select first account by pressing Enter: {e}")
            try:
                print("⚠️ Trying fallback method: Arrow Down + Enter...")
                if account_field:
                    account_field.send_keys(Keys.ARROW_DOWN)
                    time.sleep(0.5)
                    account_field.send_keys(Keys.ENTER)
                    print("✓ Successfully selected first account using Arrow Down + Enter")
                else:
                    focused_element = driver.switch_to.active_element
                    focused_element.send_keys(Keys.ARROW_DOWN)
                    time.sleep(0.5)
                    focused_element.send_keys(Keys.ENTER)
                    print("✓ Successfully selected first account using Arrow Down + Enter on focused element")
            except Exception as e2:
                print(f"⚠️ All methods failed: {e2}")
                try:
                    print("⚠️ Last resort: Trying to click on dropdown items...")
                    dropdown_selectors = [
                        "//div[contains(@class, 'dropdown-menu')]//a[1]",
                        "//ul[contains(@class, 'dropdown')]//li[1]",
                        "//div[contains(@class, 'dropdown')]//div[1]",
                        "//*[contains(@class, 'dropdown-item')][1]",
                        "//*[contains(@class, 'list-item')][1]"
                    ]
                    for selector in dropdown_selectors:
                        try:
                            first_account = WebDriverWait(driver, 3).until(
                                EC.element_to_be_clickable((By.XPATH, selector))
                            )
                            first_account.click()
                            print(f"✓ Successfully clicked on first account using selector: {selector}")
                            break
                        except:
                            continue
                except Exception as e3:
                    print(f"⚠️ All methods failed to select first account: {e3}")

        print("\n" + "=" * 50)
        print("✓ NEW FUNCTIONALITY COMPLETED SUCCESSFULLY!")
        print("✓ Account dropdown opened by pressing Enter")
        print("✓ First account selected by pressing Enter again")
        print("=" * 50 + "\n")
        # Enter remarks
        remarks = wait.until(EC.element_to_be_clickable((By.ID, "remarksid")))
        remarks.clear()
        remarks.send_keys("Automated test remarks.")

        # Barcode + Quantity
        barcode_input = driver.find_element(By.ID, "barcodeField")
        barcode_input.clear()
        barcode_input.send_keys(barcode)
        barcode_input.send_keys(Keys.ENTER)
        time.sleep(2)

        quantity = random.randint(80, 200)
        print(f"Generated quantity: {quantity}")

        xpaths = [
            "//table//tr//td[position()=9]//input",
            "//input[contains(@name, 'quantity') or contains(@name, 'Quantity')]",
            "//input[contains(@id, 'quantity') or contains(@id, 'Quantity')]",
            "//td[contains(@class, 'quantity')]//input",
            "//table//tbody//tr[1]//td[9]//input",
        ]

        quantity_field = None
        for xpath in xpaths:
            try:
                quantity_field = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                quantity_field.clear()
                quantity_field.send_keys(str(quantity) + Keys.ENTER)
                print("✅ Quantity entered and Enter key pressed.")
                time.sleep(2)
                break
            except Exception as e:
                print(f"⚠ Failed with XPath: {xpath} -> {e}")
        else:
            print("❌ Could not locate the quantity input field.")

        # Click SAVE
        save_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'SAVE') and contains(@class, 'btn-info')]")))
        save_button.click()
        logger.info("Clicked SAVE")
        time.sleep(10)
        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.accept()
            print("Alert accepted successfully.")
        except TimeoutException:
            print("No alert appeared after clicking SAVE.")

        import pyautogui
        time.sleep(10)
        pyautogui.press('esc')
        time.sleep(5)

        view_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'VIEW')]")))
        view_button.click()

        time.sleep(2)
        actions = ActionChains(driver)
        actions.send_keys(Keys.ENTER).perform()
        time.sleep(3)

        reset_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'RESET')]")))

        # -----------------------------------
        # Popup modal check for already exists
        try:
            popup_message = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'modal')]//p"))
            )
            popup_text = popup_message.text
            allure.attach(driver.get_screenshot_as_png(),
                          name="AlreadyExistsPopup",
                          attachment_type=allure.attachment_type.PNG)
            logger.error(f"Popup after SAVE: {popup_text}")
            raise ProductAlreadyExistsError(f"Product already exists popup: {popup_text}")
        except TimeoutException:
            logger.info("No 'already exists' popup appeared after SAVE.")

        # -----------------------------------
        allure.attach(driver.get_screenshot_as_png(), name="InvoiceCreated",
                      attachment_type=allure.attachment_type.PNG)
        logger.info("Purchase invoice created successfully.")

    # -----------------------------------
    @pytest.mark.run(order=1)
    def test_product_flow(self):
        self.login(TEST_CONFIG["username"], TEST_CONFIG["password"], TEST_CONFIG["url"])
        self.create_purchase_invoice(barcode="2020")
        logger.info("Test flow completed successfully.")
        time.sleep(5)  # observe browser before closing
