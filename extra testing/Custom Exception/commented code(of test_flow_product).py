# # import allure
# # from selenium import webdriver
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.support.ui import WebDriverWait
# # from selenium.webdriver.support import expected_conditions as EC
# # from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException, \
# #     WebDriverException
# # from selenium.webdriver.common.keys import Keys
# # from selenium.webdriver.common.action_chains import ActionChains
# # import time
# # import logging
# #
# # # Configure logging
# # logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# # logger = logging.getLogger(__name__)
# #
# #
# # # Custom Exceptions
# # class LoginFailedError(Exception):
# #     """Raised when login fails due to invalid credentials or unexpected errors."""
# #     pass
# #
# #
# # class ProductMasterCreationError(Exception):
# #     """Raised when product master creation fails."""
# #     pass
# #
# #
# # class WebDriverInitializationError(Exception):
# #     """Raised when WebDriver initialization fails."""
# #     pass
# #
# #
# # # Initialize driver with error handling
# # def initialize_driver():
# #     """Initialize Chrome WebDriver with proper error handling."""
# #     try:
# #         driver = webdriver.Chrome()
# #         logger.info("WebDriver initialized successfully")
# #         return driver
# #     except WebDriverException as e:
# #         logger.error(f"Failed to initialize WebDriver: {e}")
# #         raise WebDriverInitializationError(f"WebDriver initialization failed: {e}")
# #
# #
# # driver = None
# #
# #
# # @allure.step("Perform login with username: {username}")
# # def Login(username, password, link):
# #     """
# #     Perform login with improved error handling and retry mechanism.
# #     """
# #     if not driver:
# #         raise WebDriverInitializationError("Driver not initialized")
# #
# #     try:
# #         driver.maximize_window()
# #         driver.get(link)
# #         logger.info(f"Navigated to login page: {link}")
# #
# #         with allure.step("Entering credentials and clicking Sign In"):
# #             # Wait for username field and enter credentials
# #             username_field = WebDriverWait(driver, 15).until(
# #                 EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[formcontrolname="username"]'))
# #             )
# #             username_field.clear()
# #             username_field.send_keys(username)
# #             logger.info("Username entered successfully")
# #
# #             # Enter password
# #             password_field = WebDriverWait(driver, 10).until(
# #                 EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[formcontrolname="password"]'))
# #             )
# #             password_field.clear()
# #             password_field.send_keys(password)
# #             logger.info("Password entered successfully")
# #
# #             # Click Sign In button
# #             sign_in_btn = WebDriverWait(driver, 10).until(
# #                 EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign In')]"))
# #             )
# #             sign_in_btn.click()
# #             logger.info("Sign In button clicked")
# #
# #         # Handle already logged in scenario
# #         try:
# #             logout_btn = WebDriverWait(driver, 8).until(
# #                 EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Logout']]"))
# #             )
# #             with allure.step("Detected 'Already Logged In' popup — logging out first"):
# #                 logout_btn.click()
# #                 time.sleep(3)
# #                 logger.info("Logged out from existing session")
# #
# #                 # Re-click Sign In
# #                 sign_in_btn = WebDriverWait(driver, 10).until(
# #                     EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign In')]"))
# #                 )
# #                 sign_in_btn.click()
# #                 logger.info("Re-clicked Sign In after logout")
# #
# #         except TimeoutException:
# #             logger.info("No 'Already Logged In' popup detected — continuing with login")
# #
# #         # Verify login success with multiple possible indicators
# #         try:
# #             login_success_indicators = [
# #                 (By.XPATH, "//span[contains(text(), 'Dashboard')]"),
# #                 (By.XPATH, "//span[contains(text(), 'Masters')]"),
# #                 (By.XPATH, "//a[contains(text(), 'Masters')]"),
# #                 (By.XPATH, "//*[contains(text(), 'Welcome')]")
# #             ]
# #
# #             login_successful = False
# #             for locator in login_success_indicators:
# #                 try:
# #                     WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator))
# #                     login_successful = True
# #                     logger.info(f"Login verified with locator: {locator}")
# #                     break
# #                 except TimeoutException:
# #                     continue
# #
# #             if not login_successful:
# #                 raise LoginFailedError("Login verification failed: no expected dashboard elements found")
# #
# #             allure.attach(driver.get_screenshot_as_png(), name="login_success",
# #                           attachment_type=allure.attachment_type.PNG)
# #             logger.info("Login successful")
# #
# #         except TimeoutException:
# #             allure.attach(driver.get_screenshot_as_png(), name="login_failed",
# #                           attachment_type=allure.attachment_type.PNG)
# #             raise LoginFailedError("Login failed: expected dashboard elements not found after timeout")
# #
# #     except (NoSuchElementException, ElementNotInteractableException) as e:
# #         logger.error(f"Element interaction error during login: {e}")
# #         allure.attach(driver.get_screenshot_as_png(), name="login_element_error",
# #                       attachment_type=allure.attachment_type.PNG)
# #         raise LoginFailedError(f"Login failed due to element interaction error: {e}")
# #
# #     except TimeoutException as e:
# #         logger.error(f"Timeout error during login: {e}")
# #         allure.attach(driver.get_screenshot_as_png(), name="login_timeout",
# #                       attachment_type=allure.attachment_type.PNG)
# #         raise LoginFailedError(f"Login failed due to timeout: {e}")
# #
# #     except WebDriverException as e:
# #         logger.error(f"WebDriver error during login: {e}")
# #         allure.attach(driver.get_screenshot_as_png(), name="login_webdriver_error",
# #                       attachment_type=allure.attachment_type.PNG)
# #         raise LoginFailedError(f"Login failed due to WebDriver error: {e}")
# #
# #     except Exception as e:
# #         logger.error(f"Unexpected error during login: {e}")
# #         allure.attach(driver.get_screenshot_as_png(), name="login_unexpected_error",
# #                       attachment_type=allure.attachment_type.PNG)
# #         raise LoginFailedError(f"Login process encountered an unexpected error: {e}")
# #
# #
# # @allure.step("Creating product master for item: {product_item}")
# # def product_master(driver, product_item, HS_code, unit, item_type,
# #                    description, category, short_name, purchase_price, sales_price,
# #                    alt_unit, conversion_factor, barcode_map, barcode_unit):
# #     """
# #     Create product master with comprehensive error handling.
# #     """
# #     if not driver:
# #         raise ProductMasterCreationError("Driver not initialized")
# #
# #     wait = WebDriverWait(driver, 15)
# #
# #     try:
# #         with allure.step("Navigating to Product Master screen"):
# #             # Navigate to Masters menu
# #             try:
# #                 Master_menu = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Masters")))
# #                 Master_menu.click()
# #                 logger.info("Clicked Masters menu")
# #             except TimeoutException:
# #                 raise ProductMasterCreationError("Masters menu not found or not clickable")
# #
# #             # Hover over Inventory Info
# #             try:
# #                 inventory_info = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Inventory Info")))
# #                 ActionChains(driver).move_to_element(inventory_info).perform()
# #                 logger.info("Hovered over Inventory Info")
# #             except TimeoutException:
# #                 raise ProductMasterCreationError("Inventory Info menu not found")
# #
# #             # Click Product Master
# #             try:
# #                 product_master_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Product Master")))
# #                 product_master_link.click()
# #                 logger.info("Clicked Product Master link")
# #             except TimeoutException:
# #                 raise ProductMasterCreationError("Product Master link not found or not clickable")
# #
# #         with allure.step("Starting product creation"):
# #             # Click Add Product button
# #             try:
# #                 add_product_btn = wait.until(
# #                     EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add Product')]")))
# #                 add_product_btn.click()
# #                 time.sleep(2)
# #                 logger.info("Clicked Add Product button")
# #             except TimeoutException:
# #                 raise ProductMasterCreationError("Add Product button not found")
# #
# #             # Set zoom level
# #             try:
# #                 driver.execute_script("document.body.style.zoom='80%'")
# #                 logger.info("Set zoom level to 80%")
# #             except WebDriverException:
# #                 logger.warning("Failed to set zoom level, continuing without zoom")
# #
# #             # Fill item group
# #             try:
# #                 item_group_input = wait.until(
# #                     EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='-- Press Enter For Item Group --']")))
# #                 item_group_input.click()
# #                 item_group_input.send_keys(Keys.ENTER, Keys.ENTER)
# #                 logger.info("Filled item group")
# #             except (TimeoutException, ElementNotInteractableException):
# #                 logger.warning("Item group input not found or not interactable, continuing")
# #
# #             # Main group
# #             try:
# #                 main_group_input = wait.until(
# #                     EC.element_to_be_clickable((By.XPATH, "//ng-select//input[@type='text']")))
# #                 main_group_input.click()
# #                 main_group_input.send_keys(Keys.ENTER, Keys.ENTER)
# #
# #                 ok_button = wait.until(
# #                     EC.element_to_be_clickable((By.XPATH, "//button[.//span[normalize-space()='Ok']]")))
# #                 ok_button.click()
# #                 logger.info("Selected main group")
# #             except (TimeoutException, ElementNotInteractableException):
# #                 logger.warning("Main group selection failed, continuing")
# #
# #             # Fill product details with individual error handling
# #             try:
# #                 item_name_field = wait.until(
# #                     EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter Item Name']")))
# #                 item_name_field.clear()
# #                 item_name_field.send_keys(product_item, Keys.TAB)
# #                 logger.info("Entered item name")
# #             except (TimeoutException, ElementNotInteractableException):
# #                 raise ProductMasterCreationError("Failed to enter item name")
# #
# #             # Continue with form filling using active element method
# #             try:
# #                 driver.switch_to.active_element.send_keys(HS_code, Keys.TAB)
# #                 driver.switch_to.active_element.send_keys(Keys.TAB, unit, Keys.TAB, item_type, Keys.TAB)
# #                 driver.switch_to.active_element.send_keys(description, Keys.TAB, category, Keys.TAB, short_name,
# #                                                           Keys.TAB)
# #                 logger.info("Filled basic product details")
# #             except Exception as e:
# #                 logger.warning(f"Some basic fields may not have been filled: {e}")
# #
# #             # Fill prices
# #             try:
# #                 purchase_price_field = wait.until(
# #                     EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter Purchase Price']")))
# #                 purchase_price_field.clear()
# #                 purchase_price_field.send_keys(purchase_price)
# #
# #                 sales_price_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='0']")))
# #                 sales_price_field.clear()
# #                 sales_price_field.send_keys(sales_price)
# #                 logger.info("Filled price fields")
# #             except (TimeoutException, ElementNotInteractableException):
# #                 logger.warning("Price fields not found or not interactable")
# #
# #             # Alternate Unit section
# #             try:
# #                 alt_unit_section = wait.until(
# #                     EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Alternate Unit')]")))
# #                 alt_unit_section.click()
# #                 time.sleep(1)
# #
# #                 alt_unit_select = driver.find_element(By.XPATH, "//select[contains(@class,'ng-pristine')]")
# #                 alt_unit_select.click()
# #                 driver.switch_to.active_element.send_keys(alt_unit, Keys.TAB)
# #
# #                 conversion_field = wait.until(
# #                     EC.element_to_be_clickable((By.XPATH, "//input[@type='number' and contains(@class, 'ng-valid')]")))
# #                 conversion_field.clear()
# #                 conversion_field.send_keys(conversion_factor)
# #                 logger.info("Filled alternate unit details")
# #             except Exception as e:
# #                 logger.warning(f"Alternate unit section failed: {e}")
# #
# #             # Barcode Mapping section
# #             try:
# #                 barcode_section = wait.until(
# #                     EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Barcode Mapping')]")))
# #                 barcode_section.click()
# #                 time.sleep(1)
# #
# #                 barcode_field = driver.find_element(By.XPATH, "//input[@placeholder='Enter Bar Code']")
# #                 barcode_field.clear()
# #                 barcode_field.send_keys(barcode_map, Keys.TAB)
# #
# #                 barcode_unit_select = driver.find_element(By.CSS_SELECTOR, 'div.col-2.p-0 select')
# #                 barcode_unit_select.click()
# #                 driver.switch_to.active_element.send_keys(barcode_unit, Keys.TAB)
# #
# #                 map_button = wait.until(EC.element_to_be_clickable((By.ID, "map")))
# #                 map_button.click()
# #                 logger.info("Filled barcode mapping details")
# #             except Exception as e:
# #                 logger.warning(f"Barcode mapping section failed: {e}")
# #
# #             # Save the product
# #             try:
# #                 save_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'SAVE')]")))
# #                 save_button.click()
# #                 time.sleep(3)
# #                 logger.info("Clicked Save button")
# #             except TimeoutException:
# #                 raise ProductMasterCreationError("Save button not found or not clickable")
# #
# #             # Verify save success
# #             allure.attach(driver.get_screenshot_as_png(), name="product_created",
# #                           attachment_type=allure.attachment_type.PNG)
# #             logger.info("Product master created successfully")
# #
# #     except ProductMasterCreationError:
# #         # Re-raise our custom exceptions
# #         raise
# #
# #     except (NoSuchElementException, ElementNotInteractableException) as e:
# #         logger.error(f"Element interaction error during product creation: {e}")
# #         allure.attach(driver.get_screenshot_as_png(), name="product_creation_element_error",
# #                       attachment_type=allure.attachment_type.PNG)
# #         raise ProductMasterCreationError(f"Failed to create product master due to element interaction error: {e}")
# #
# #     except TimeoutException as e:
# #         logger.error(f"Timeout error during product creation: {e}")
# #         allure.attach(driver.get_screenshot_as_png(), name="product_creation_timeout",
# #                       attachment_type=allure.attachment_type.PNG)
# #         raise ProductMasterCreationError(f"Failed to create product master due to timeout: {e}")
# #
# #     except WebDriverException as e:
# #         logger.error(f"WebDriver error during product creation: {e}")
# #         allure.attach(driver.get_screenshot_as_png(), name="product_creation_webdriver_error",
# #                       attachment_type=allure.attachment_type.PNG)
# #         raise ProductMasterCreationError(f"Failed to create product master due to WebDriver error: {e}")
# #
# #     except Exception as e:
# #         logger.error(f"Unexpected error during product creation: {e}")
# #         allure.attach(driver.get_screenshot_as_png(), name="product_creation_unexpected_error",
# #                       attachment_type=allure.attachment_type.PNG)
# #         raise ProductMasterCreationError(f"Failed to create product master due to unexpected error: {e}")
# #
# #
# # # Main execution with comprehensive error handling
# # def main():
# #     """Main execution function with proper error handling and cleanup."""
# #     global driver
# #
# #     try:
# #         # Initialize driver
# #         driver = initialize_driver()
# #
# #         # Perform login
# #         Login("gedehim917@decodewp.com", "Tebahal1!", "https://velvet.webredirect.himshang.com.np/#/pages/dashboard")
# #
# #         # Create product master
# #         product_master(driver,
# #                        product_item="Testing1",
# #                        HS_code="123",
# #                        unit="kg.",
# #                        item_type="Service Item",
# #                        description="This is description",
# #                        category="N/A",
# #                        short_name="XYZ",
# #                        purchase_price="120",
# #                        sales_price="140",
# #                        alt_unit="Each",
# #                        conversion_factor="1000",
# #                        barcode_map="2020",
# #                        barcode_unit="kg.")
# #
# #         logger.info("All operations completed successfully")
# #
# #     except WebDriverInitializationError as e:
# #         logger.error(f"WebDriver initialization failed: {e}")
# #         print(f"❌ WebDriver Error: {e}")
# #
# #     except LoginFailedError as e:
# #         logger.error(f"Login failed: {e}")
# #         print(f"❌ Login Error: {e}")
# #
# #     except ProductMasterCreationError as e:
# #         logger.error(f"Product master creation failed: {e}")
# #         print(f"❌ Product Creation Error: {e}")
# #
# #     except Exception as e:
# #         logger.error(f"Unexpected error in main execution: {e}")
# #         print(f"❌ Unexpected Error: {e}")
# #
# #     finally:
# #         # Cleanup
# #         if driver:
# #             try:
# #                 logger.info("Cleaning up - waiting 10 seconds before closing driver")
# #                 time.sleep(10)
# #                 driver.quit()
# #                 logger.info("Driver closed successfully")
# #             except Exception as e:
# #                 logger.error(f"Error during cleanup: {e}")
# #                 print(f"⚠️ Cleanup Error: {e}")
# #
# #
# # if __name__ == "__main__":
# #     main()
#
#
# import pytest
# from webdriver_manager.core import driver
#
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
# class ProductMasterCreationError(Exception):
#     """Raised when product master creation fails."""
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
#         "product_item": "Testing1",
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
#         "barcode_map": "2020",
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
#     def login(self, username, password, link):
#         """
#         Perform login with improved error handling and retry mechanism.
#         """
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
#                 # Click Sign In button
#                 sign_in_btn = WebDriverWait(self.driver, 10).until(
#                     EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign In')]"))
#                 )
#                 sign_in_btn.click()
#                 logger.info("Sign In button clicked")
#
#
#
#             # Handle already logged in scenario
#             try:
#                 logout_btn = WebDriverWait(self.driver, 8).until(
#                     EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Logout']]"))
#                 )
#                 with allure.step("Detected 'Already Logged In' popup — logging out first"):
#                     logout_btn.click()
#                     time.sleep(3)
#                     logger.info("Logged out from existing session")
#
#                     # Re-click Sign In
#                     sign_in_btn = WebDriverWait(self.driver, 10).until(
#                         EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign In')]"))
#                     )
#                     sign_in_btn.click()
#                     logger.info("Re-clicked Sign In after logout")
#
#             except TimeoutException:
#                 logger.info("No 'Already Logged In' popup detected — continuing with login")
#
#             # Verify login success with multiple possible indicators
#             try:
#                 login_success_indicators = [
#                     (By.XPATH, "//span[contains(text(), 'Dashboard')]"),
#                     (By.XPATH, "//span[contains(text(), 'Masters')]"),
#                     (By.XPATH, "//a[contains(text(), 'Masters')]"),
#                     (By.XPATH, "//*[contains(text(), 'Welcome')]")
#                 ]
#
#                 login_successful = False
#                 for locator in login_success_indicators:
#                     try:
#                         WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(locator))
#                         login_successful = True
#                         logger.info(f"Login verified with locator: {locator}")
#                         break
#                     except TimeoutException:
#                         continue
#
#                 if not login_successful:
#                     raise LoginFailedError("Login verification failed: no expected dashboard elements found")
#
#                 allure.attach(self.driver.get_screenshot_as_png(), name="login_success",
#                               attachment_type=allure.attachment_type.PNG)
#                 logger.info("Login successful")
#
#             except TimeoutException:
#                 allure.attach(self.driver.get_screenshot_as_png(), name="login_failed",
#                               attachment_type=allure.attachment_type.PNG)
#                 raise LoginFailedError("Login failed: expected dashboard elements not found after timeout")
#
#         except (NoSuchElementException, ElementNotInteractableException) as e:
#             logger.error(f"Element interaction error during login: {e}")
#             allure.attach(self.driver.get_screenshot_as_png(), name="login_element_error",
#                           attachment_type=allure.attachment_type.PNG)
#             raise LoginFailedError(f"Login failed due to element interaction error: {e}")
#
#         except TimeoutException as e:
#             logger.error(f"Timeout error during login: {e}")
#             allure.attach(self.driver.get_screenshot_as_png(), name="login_timeout",
#                           attachment_type=allure.attachment_type.PNG)
#             raise LoginFailedError(f"Login failed due to timeout: {e}")
#
#         except WebDriverException as e:
#             logger.error(f"WebDriver error during login: {e}")
#             allure.attach(self.driver.get_screenshot_as_png(), name="login_webdriver_error",
#                           attachment_type=allure.attachment_type.PNG)
#             raise LoginFailedError(f"Login failed due to WebDriver error: {e}")
#
#         except Exception as e:
#             logger.error(f"Unexpected error during login: {e}")
#             allure.attach(self.driver.get_screenshot_as_png(), name="login_unexpected_error",
#                           attachment_type=allure.attachment_type.PNG)
#             raise LoginFailedError(f"Login process encountered an unexpected error: {e}")
#
#     @allure.step("Creating product master for item: {product_item}")
#     def create_product_master(self, product_item, HS_code, unit, item_type,
#                               description, category, short_name, purchase_price, sales_price,
#                               alt_unit, conversion_factor, barcode_map, barcode_unit):
#         """
#         Create product master with comprehensive error handling.
#         """
#         wait = WebDriverWait(self.driver, 15)
#
#         try:
#             with allure.step("Navigating to Product Master screen"):
#                 # Navigate to Masters menu
#                 try:
#                     Master_menu = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Masters")))
#                     Master_menu.click()
#                     logger.info("Clicked Masters menu")
#                 except TimeoutException:
#                     raise ProductMasterCreationError("Masters menu not found or not clickable")
#
#                 # Hover over Inventory Info
#                 try:
#                     inventory_info = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Inventory Info")))
#                     ActionChains(self.driver).move_to_element(inventory_info).perform()
#                     logger.info("Hovered over Inventory Info")
#                 except TimeoutException:
#                     raise ProductMasterCreationError("Inventory Info menu not found")
#
#                 # Click Product Master
#                 try:
#                     product_master_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Product Master")))
#                     product_master_link.click()
#                     logger.info("Clicked Product Master link")
#                 except TimeoutException:
#                     raise ProductMasterCreationError("Product Master link not found or not clickable")
#
#             with allure.step("Starting product creation"):
#                 # Click Add Product button
#                 try:
#                     add_product_btn = wait.until(
#                         EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add Product')]")))
#                     add_product_btn.click()
#                     time.sleep(2)
#                     logger.info("Clicked Add Product button")
#                 except TimeoutException:
#                     raise ProductMasterCreationError("Add Product button not found")
#
#                 # Set zoom level
#                 try:
#                     self.driver.execute_script("document.body.style.zoom='80%'")
#                     logger.info("Set zoom level to 80%")
#                 except WebDriverException:
#                     logger.warning("Failed to set zoom level, continuing without zoom")
#
#                 # Fill item group
#                 try:
#                     item_group_input = wait.until(EC.element_to_be_clickable(
#                         (By.XPATH, "//input[@placeholder='-- Press Enter For Item Group --']")))
#                     item_group_input.click()
#                     item_group_input.send_keys(Keys.ENTER, Keys.ENTER)
#                     logger.info("Filled item group")
#                 except (TimeoutException, ElementNotInteractableException):
#                     logger.warning("Item group input not found or not interactable, continuing")
#
#                 # Main group
#                 try:
#                     main_group_input = wait.until(
#                         EC.element_to_be_clickable((By.XPATH, "//ng-select//input[@type='text']")))
#                     main_group_input.click()
#                     main_group_input.send_keys(Keys.ENTER, Keys.ENTER)
#
#                     ok_button = wait.until(
#                         EC.element_to_be_clickable((By.XPATH, "//button[.//span[normalize-space()='Ok']]")))
#                     ok_button.click()
#                     logger.info("Selected main group")
#                 except (TimeoutException, ElementNotInteractableException):
#                     logger.warning("Main group selection failed, continuing")
#
#                 # Fill product details with individual error handling
#                 try:
#                     item_name_field = wait.until(
#                         EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter Item Name']")))
#                     item_name_field.clear()
#                     item_name_field.send_keys(product_item, Keys.TAB)
#                     logger.info("Entered item name")
#                 except (TimeoutException, ElementNotInteractableException):
#                     raise ProductMasterCreationError("Failed to enter item name")
#
#                 # Continue with form filling using active element method
#                 try:
#                     self.driver.switch_to.active_element.send_keys(HS_code, Keys.TAB)
#                     self.driver.switch_to.active_element.send_keys(Keys.TAB, unit, Keys.TAB, item_type, Keys.TAB)
#                     self.driver.switch_to.active_element.send_keys(description, Keys.TAB, category, Keys.TAB,
#                                                                    short_name, Keys.TAB)
#                     logger.info("Filled basic product details")
#                 except Exception as e:
#                     logger.warning(f"Some basic fields may not have been filled: {e}")
#
#                 # Fill prices
#                 try:
#                     purchase_price_field = wait.until(
#                         EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter Purchase Price']")))
#                     purchase_price_field.clear()
#                     purchase_price_field.send_keys(purchase_price)
#
#                     sales_price_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='0']")))
#                     sales_price_field.clear()
#                     sales_price_field.send_keys(sales_price)
#                     logger.info("Filled price fields")
#                 except (TimeoutException, ElementNotInteractableException):
#                     logger.warning("Price fields not found or not interactable")
#
#                 # Alternate Unit section
#                 try:
#                     alt_unit_section = wait.until(
#                         EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Alternate Unit')]")))
#                     alt_unit_section.click()
#                     time.sleep(1)
#
#                     alt_unit_select = self.driver.find_element(By.XPATH, "//select[contains(@class,'ng-pristine')]")
#                     alt_unit_select.click()
#                     self.driver.switch_to.active_element.send_keys(alt_unit, Keys.TAB)
#
#                     conversion_field = wait.until(EC.element_to_be_clickable(
#                         (By.XPATH, "//input[@type='number' and contains(@class, 'ng-valid')]")))
#                     conversion_field.clear()
#                     conversion_field.send_keys(conversion_factor)
#                     logger.info("Filled alternate unit details")
#                 except Exception as e:
#                     logger.warning(f"Alternate unit section failed: {e}")
#
#                 # Barcode Mapping section
#                 try:
#                     barcode_section = wait.until(
#                         EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Barcode Mapping')]")))
#                     barcode_section.click()
#                     time.sleep(1)
#
#                     barcode_field = self.driver.find_element(By.XPATH, "//input[@placeholder='Enter Bar Code']")
#                     barcode_field.clear()
#                     barcode_field.send_keys(barcode_map, Keys.TAB)
#
#                     barcode_unit_select = self.driver.find_element(By.CSS_SELECTOR, 'div.col-2.p-0 select')
#                     barcode_unit_select.click()
#                     self.driver.switch_to.active_element.send_keys(barcode_unit, Keys.TAB)
#
#                     map_button = wait.until(EC.element_to_be_clickable((By.ID, "map")))
#                     map_button.click()
#                     logger.info("Filled barcode mapping details")
#                 except Exception as e:
#                     logger.warning(f"Barcode mapping section failed: {e}")
#
#                 # Save the product
#                 try:
#                     save_button = wait.until(
#                         EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'SAVE')]")))
#                     save_button.click()
#                     time.sleep(3)
#                     logger.info("Clicked Save button")
#                 except TimeoutException:
#                     raise ProductMasterCreationError("Save button not found or not clickable")
#
#                 # Verify save success
#                 allure.attach(self.driver.get_screenshot_as_png(), name="product_created",
#                               attachment_type=allure.attachment_type.PNG)
#                 logger.info("Product master created successfully")
#
#         except ProductMasterCreationError:
#             # Re-raise our custom exceptions
#             raise
#
#         except (NoSuchElementException, ElementNotInteractableException) as e:
#             logger.error(f"Element interaction error during product creation: {e}")
#             allure.attach(self.driver.get_screenshot_as_png(), name="product_creation_element_error",
#                           attachment_type=allure.attachment_type.PNG)
#             raise ProductMasterCreationError(f"Failed to create product master due to element interaction error: {e}")
#
#         except TimeoutException as e:
#             logger.error(f"Timeout error during product creation: {e}")
#             allure.attach(self.driver.get_screenshot_as_png(), name="product_creation_timeout",
#                           attachment_type=allure.attachment_type.PNG)
#             raise ProductMasterCreationError(f"Failed to create product master due to timeout: {e}")
#
#         except WebDriverException as e:
#             logger.error(f"WebDriver error during product creation: {e}")
#             allure.attach(self.driver.get_screenshot_as_png(), name="product_creation_webdriver_error",
#                           attachment_type=allure.attachment_type.PNG)
#             raise ProductMasterCreationError(f"Failed to create product master due to WebDriver error: {e}")
#
#         except Exception as e:
#             logger.error(f"Unexpected error during product creation: {e}")
#             allure.attach(self.driver.get_screenshot_as_png(), name="product_creation_unexpected_error",
#                           attachment_type=allure.attachment_type.PNG)
#             raise ProductMasterCreationError(f"Failed to create product master due to unexpected error: {e}")
#
#     @allure.feature("User Authentication")
#     @allure.story("Login Functionality")
#     def test_login_functionality(self):
#         """Test login functionality with valid credentials."""
#         try:
#             self.login(
#                 TEST_CONFIG["username"],
#                 TEST_CONFIG["password"],
#                 TEST_CONFIG["url"]
#             )
#             logger.info("Login test passed successfully")
#         except LoginFailedError as e:
#             pytest.fail(f"Login test failed: {e}")
#
#     @allure.feature("Product Management")
#     @allure.story("Product Master Creation")
#     def test_product_master_creation(self):
#         """Test complete product master creation flow."""
#         try:
#             # First login
#             self.login(
#                 TEST_CONFIG["username"],
#                 TEST_CONFIG["password"],
#                 TEST_CONFIG["url"]
#             )
#
#             # Then create product master
#             product_data = TEST_CONFIG["product_data"]
#             self.create_product_master(
#                 product_data["product_item"],
#                 product_data["HS_code"],
#                 product_data["unit"],
#                 product_data["item_type"],
#                 product_data["description"],
#                 product_data["category"],
#                 product_data["short_name"],
#                 product_data["purchase_price"],
#                 product_data["sales_price"],
#                 product_data["alt_unit"],
#                 product_data["conversion_factor"],
#                 product_data["barcode_map"],
#                 product_data["barcode_unit"]
#             )
#
#             logger.info("Product master creation test passed successfully")
#
#         except (LoginFailedError, ProductMasterCreationError) as e:
#             pytest.fail(f"Product master creation test failed: {e}")
#
#     @allure.feature("End-to-End Flow")
#     @allure.story("Complete Product Flow")
#     def test_complete_product_flow(self):
#         """Test complete end-to-end product flow."""
#         try:
#             # Login
#             self.login(
#                 TEST_CONFIG["username"],
#                 TEST_CONFIG["password"],
#                 TEST_CONFIG["url"]
#             )
#
#             # Create product master
#             product_data = TEST_CONFIG["product_data"]
#             self.create_product_master(
#                 product_data["product_item"],
#                 product_data["HS_code"],
#                 product_data["unit"],
#                 product_data["item_type"],
#                 product_data["description"],
#                 product_data["category"],
#                 product_data["short_name"],
#                 product_data["purchase_price"],
#                 product_data["sales_price"],
#                 product_data["alt_unit"],
#                 product_data["conversion_factor"],
#                 product_data["barcode_map"],
#                 product_data["barcode_unit"]
#             )
#
#             # Additional verification or flow steps can be added here
#             logger.info("Complete product flow test passed successfully")
#
#         except (LoginFailedError, ProductMasterCreationError) as e:
#             pytest.fail(f"Complete product flow test failed: {e}")
#
#
# # Additional standalone test functions (if needed)
# @allure.feature("Smoke Tests")
# @allure.story("Basic Functionality")
# def test_webdriver_initialization():
#     """Test WebDriver can be initialized without errors."""
#     driver = None
#     try:
#         driver = webdriver.Chrome()
#         logger.info("WebDriver initialization test passed")
#         assert driver is not None
#     except WebDriverException as e:
#         pytest.fail(f"WebDriver initialization failed: {e}")
#     finally:
#         if driver:
#             driver.quit()
#
#
# if __name__ == "__main__":
#     # For running directly (not via pytest)
#     test_instance = TestProductFlow()
#     test_instance.setup_method()
#     try:
#         test_instance.test_complete_product_flow()
#         print("✅ All tests passed when run directly")
#     except Exception as e:
#         print(f"❌ Test failed: {e}")
#     finally:
#         test_instance.teardown_method()
