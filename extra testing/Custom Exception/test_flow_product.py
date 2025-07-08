import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException, \
    WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Custom Exceptions
class LoginFailedError(Exception):
    """Raised when login fails due to invalid credentials or unexpected errors."""
    pass


class ProductMasterCreationError(Exception):
    """Raised when product master creation fails."""
    pass


class WebDriverInitializationError(Exception):
    """Raised when WebDriver initialization fails."""
    pass


# Test Configuration
TEST_CONFIG = {
    "username": "gedehim917@decodewp.com",
    "password": "Tebahal1!",
    "url": "https://velvet.webredirect.himshang.com.np/#/pages/dashboard",
    "product_data": {
        "product_item": "Testing10",
        "HS_code": "123",
        "unit": "kg.",
        "item_type": "Service Item",
        "description": "This is description",
        "category": "N/A",
        "short_name": "XYZ",
        "purchase_price": "120",
        "sales_price": "140",
        "alt_unit": "Each",
        "conversion_factor": "1000",
        "barcode_map": "20",
        "barcode_unit": "kg."
    }
}


class TestProductFlow:
    """Test class for product flow automation."""

    def setup_method(self):
        """Setup method that runs before each test method."""
        try:
            self.driver = webdriver.Chrome()
            self.driver.implicitly_wait(10)
            logger.info("WebDriver initialized successfully")
        except WebDriverException as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise WebDriverInitializationError(f"WebDriver initialization failed: {e}")

    def safe_click(self, element, description="element"):
        """
        Safely click an element with fallback methods.

        Args:
            element: WebElement to click
            description: Description of the element for logging
        """
        try:
            element.click()
            logger.info(f"Clicked {description} using regular click")
        except Exception as e:
            logger.warning(f"Regular click failed for {description}, trying JavaScript click: {e}")
            try:
                self.driver.execute_script("arguments[0].click();", element)
                logger.info(f"Clicked {description} using JavaScript click")
            except Exception as js_error:
                logger.error(f"JavaScript click also failed for {description}: {js_error}")
                raise ElementNotInteractableException(
                    f"Failed to click {description} using both regular and JavaScript methods")

    def teardown_method(self):
        """Teardown method that runs after each test method."""
        if hasattr(self, 'driver') and self.driver:
            try:
                logger.info("Cleaning up - closing driver")
                self.driver.quit()
                logger.info("Driver closed successfully")
            except Exception as e:
                logger.error(f"Error during cleanup: {e}")

    @allure.step("Perform login with username: {username}")
    @pytest.hookimpl(hookwrapper=True)
    def login(self, username, password, link):
        """
        Perform login with improved error handling and retry mechanism.
        """
        try:
            self.driver.maximize_window()
            self.driver.get(link)
            logger.info(f"Navigated to login page: {link}")

            with allure.step("Entering credentials and clicking Sign In"):
                # Wait for username field and enter credentials
                username_field = WebDriverWait(self.driver, 15).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[formcontrolname="username"]'))
                )
                username_field.clear()
                username_field.send_keys(username)
                logger.info("Username entered successfully")

                # Enter password
                password_field = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[formcontrolname="password"]'))
                )
                password_field.clear()
                password_field.send_keys(password)
                logger.info("Password entered successfully")

                # Click Sign In button with fallback methods
                sign_in_btn = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign In')]"))
                )
                self.safe_click(sign_in_btn, "Sign In button")

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

            # Verify login success with multiple possible indicators
            try:
                login_success_indicators = [
                    (By.XPATH, "//span[contains(text(), 'Dashboard')]"),
                    (By.XPATH, "//span[contains(text(), 'Masters')]"),
                    (By.XPATH, "//a[contains(text(), 'Masters')]"),
                    (By.XPATH, "//*[contains(text(), 'Welcome')]")
                ]

                login_successful = False
                for locator in login_success_indicators:
                    try:
                        WebDriverWait(self.driver, 5).until(EC.presence_of_element_located(locator))
                        login_successful = True
                        logger.info(f"Login verified with locator: {locator}")
                        break
                    except TimeoutException:
                        continue

                if not login_successful:
                    raise LoginFailedError("Login verification failed: no expected dashboard elements found")

                allure.attach(self.driver.get_screenshot_as_png(), name="login_success",
                              attachment_type=allure.attachment_type.PNG)
                logger.info("Login successful")

            except TimeoutException:
                allure.attach(self.driver.get_screenshot_as_png(), name="login_failed",
                              attachment_type=allure.attachment_type.PNG)
                raise LoginFailedError("Login failed: expected dashboard elements not found after timeout")

        except (NoSuchElementException, ElementNotInteractableException) as e:
            logger.error(f"Element interaction error during login: {e}")
            allure.attach(self.driver.get_screenshot_as_png(), name="login_element_error",
                          attachment_type=allure.attachment_type.PNG)
            raise LoginFailedError(f"Login failed due to element interaction error: {e}")

        except TimeoutException as e:
            logger.error(f"Timeout error during login: {e}")
            allure.attach(self.driver.get_screenshot_as_png(), name="login_timeout",
                          attachment_type=allure.attachment_type.PNG)
            raise LoginFailedError(f"Login failed due to timeout: {e}")

        except WebDriverException as e:
            logger.error(f"WebDriver error during login: {e}")
            allure.attach(self.driver.get_screenshot_as_png(), name="login_webdriver_error",
                          attachment_type=allure.attachment_type.PNG)
            raise LoginFailedError(f"Login failed due to WebDriver error: {e}")

        except Exception as e:
            logger.error(f"Unexpected error during login: {e}")
            allure.attach(self.driver.get_screenshot_as_png(), name="login_unexpected_error",
                          attachment_type=allure.attachment_type.PNG)
            raise LoginFailedError(f"Login process encountered an unexpected error: {e}")

    @allure.step("Creating product master for item: {product_item}")
    @pytest.hookimpl(hookwrapper=True)
    def create_product_master(self, product_item, HS_code, unit, item_type,
                              description, category, short_name, purchase_price, sales_price,
                              alt_unit, conversion_factor, barcode_map, barcode_unit):
        """
        Create product master with comprehensive error handling.
        """
        wait = WebDriverWait(self.driver, 15)

        try:
            with allure.step("Navigating to Product Master screen"):
                # Navigate to Masters menu
                try:
                    Master_menu = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Masters")))
                    Master_menu.click()
                    logger.info("Clicked Masters menu")
                except TimeoutException:
                    raise ProductMasterCreationError("Masters menu not found or not clickable")

                # Hover over Inventory Info
                try:
                    inventory_info = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Inventory Info")))
                    ActionChains(self.driver).move_to_element(inventory_info).perform()
                    logger.info("Hovered over Inventory Info")
                except TimeoutException:
                    raise ProductMasterCreationError("Inventory Info menu not found")

                # Click Product Master
                try:
                    product_master = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Product Master")))
                    product_master.click()
                    print("Clicked 'Product Master'")
                    time.sleep(5)

                    # Click on "Add Product" button
                    back_btn = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add Product')]")))
                    back_btn.click()
                    time.sleep(10)


                    add_product = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'Add Product')]")))
                    # Click the "Add Product" label
                    add_product.click()
                    time.sleep(5)

                except TimeoutException:
                    raise ProductMasterCreationError("Product Master link not found or not clickable")
                # try:
                #    add _product = wait.until(
                #         EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'Add Product')]")))
                #     # Click the "Add Product" label
                #     add_product.click()
                #     time.sleep(5)
                # except TimeoutException:
                #     raise ProductMasterCreationError("Product Master link not found or not clickable")

            # with allure.step("Starting product creation"):
            #     # Click Add Product button with fallback
            #     try:
            #         add_product_btn = wait.until(
            #             EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add Product')]")))
            #         self.safe_click(add_product_btn, "Add Product button")
            #         time.sleep(2)
            #     except TimeoutException:
            #         raise ProductMasterCreationError("Add Product button not found")

                # Set zoom level
                try:
                    self.driver.execute_script("document.body.style.zoom='80%'")
                    logger.info("Set zoom level to 80%")
                except WebDriverException:
                    logger.warning("Failed to set zoom level, continuing without zoom")

                # Fill item group
                try:
                    # item_group_input = wait.until(EC.element_to_be_clickable(
                    #     (By.XPATH, "//input[@placeholder='-- Press Enter For Item Group --']")))
                    # item_group_input.click()
                    # item_group_input.send_keys(Keys.ENTER, Keys.ENTER)
                    # logger.info("Filled item group")
                    item_group_input = wait.until(EC.element_to_be_clickable(
                        (By.XPATH, "//input[@placeholder='-- Press Enter For Item Group --']")))
                    item_group_input.click()
                    time.sleep(5)
                    # Press Enter on the Item Group field
                    item_group_input.send_keys(Keys.ENTER)
                    time.sleep(5)

                    # wait = WebDriverWait(driver, 5)

                    # Find and click the main group input field
                    main_group_input = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//ng-select//input[@type='text']")))
                    main_group_input.click()
                    # Send Enter key to trigger dropdown
                    main_group_input.send_keys(Keys.ENTER)
                    # Send Enter again to select the first dropdown option
                    main_group_input.send_keys(Keys.ENTER)
                    main_group_input.send_keys(Keys.ENTER)

                    time.sleep(8)

                    ok_button = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[.//span[normalize-space()='Ok']]")))
                    ok_button.click()


                except (TimeoutException, ElementNotInteractableException):
                    logger.warning("Item group input not found or not interactable, continuing")

                # # Main group
                # try:
                #     main_group_input = wait.until(
                #         EC.element_to_be_clickable((By.XPATH, "//ng-select//input[@type='text']")))
                #     main_group_input.click()
                #     main_group_input.send_keys(Keys.ENTER, Keys.ENTER)
                #
                #     ok_button = wait.until(
                #         EC.element_to_be_clickable((By.XPATH, "//button[.//span[normalize-space()='Ok']]")))
                #     ok_button.click()
                #     logger.info("Selected main group")
                # except (TimeoutException, ElementNotInteractableException):
                #     logger.warning("Main group selection failed, continuing")

                # Fill product details with individual error handling
                try:
                    item_name_field = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter Item Name']")))
                    item_name_field.clear()
                    item_name_field.send_keys(product_item, Keys.TAB)
                    logger.info("Entered item name")
                except (TimeoutException, ElementNotInteractableException):
                    raise ProductMasterCreationError("Failed to enter item name")

                # Continue with form filling using active element method
                try:
                    self.driver.switch_to.active_element.send_keys(HS_code, Keys.TAB)
                    self.driver.switch_to.active_element.send_keys(Keys.TAB, unit, Keys.TAB, item_type, Keys.TAB)
                    self.driver.switch_to.active_element.send_keys(description, Keys.TAB, category, Keys.TAB,
                                                                   short_name, Keys.TAB)
                    logger.info("Filled basic product details")
                except Exception as e:
                    logger.warning(f"Some basic fields may not have been filled: {e}")

                # Fill prices
                try:
                    purchase_price_field = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter Purchase Price']")))
                    purchase_price_field.clear()
                    purchase_price_field.send_keys(purchase_price)

                    sales_price_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='0']")))
                    sales_price_field.clear()
                    sales_price_field.send_keys(sales_price)
                    logger.info("Filled price fields")
                except (TimeoutException, ElementNotInteractableException):
                    logger.warning("Price fields not found or not interactable")

                # Alternate Unit section
                try:
                    alt_unit_section = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Alternate Unit')]")))
                    alt_unit_section.click()
                    time.sleep(1)

                    alt_unit_select = self.driver.find_element(By.XPATH, "//select[contains(@class,'ng-pristine')]")
                    alt_unit_select.click()
                    self.driver.switch_to.active_element.send_keys(alt_unit, Keys.TAB)

                    conversion_field = wait.until(EC.element_to_be_clickable(
                        (By.XPATH, "//input[@type='number' and contains(@class, 'ng-valid')]")))
                    conversion_field.clear()
                    conversion_field.send_keys(conversion_factor)
                    logger.info("Filled alternate unit details")
                except Exception as e:
                    logger.warning(f"Alternate unit section failed: {e}")

                # Barcode Mapping section
                try:
                    barcode_section = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Barcode Mapping')]")))
                    barcode_section.click()
                    time.sleep(1)

                    barcode_field = self.driver.find_element(By.XPATH, "//input[@placeholder='Enter Bar Code']")
                    barcode_field.clear()
                    barcode_field.send_keys(barcode_map, Keys.TAB)

                    barcode_unit_select = self.driver.find_element(By.CSS_SELECTOR, 'div.col-2.p-0 select')
                    barcode_unit_select.click()
                    self.driver.switch_to.active_element.send_keys(barcode_unit, Keys.TAB)

                    map_button = wait.until(EC.element_to_be_clickable((By.ID, "map")))
                    map_button.click()
                    logger.info("Filled barcode mapping details")
                except Exception as e:
                    logger.warning(f"Barcode mapping section failed: {e}")

                # Save the product with fallback clicking methods
                # try:
                #     save_button = wait.until(
                #         EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'SAVE')]")))
                #     self.safe_click(save_button, "Save button")
                #     time.sleep(3)
                # except TimeoutException:
                #     raise ProductMasterCreationError("Save button not found or not clickable")
                # # for popup
                # try:
                #     # wait for popup (you can adjust the locator as per your popup)
                #     popup = WebDriverWait(self.driver, 5).until(
                #         EC.visibility_of_element_located((By.XPATH, "//div[@class='popup']"))
                #     )
                #
                #     # take screenshot and attach to allure
                #     allure.attach(self.driver.get_screenshot_as_png(), name="Popup Screenshot",
                #                   attachment_type=allure.attachment_type.PNG)
                #
                #     # raise exception so test fails
                #     raise Exception("Unexpected popup appeared while saving the product.")
                #
                # except TimeoutException:
                #     # no popup found, continue
                #     pass
                #
                # # Verify save success
                # allure.attach(self.driver.get_screenshot_as_png(), name="product_created",
                #               attachment_type=allure.attachment_type.PNG)
                # logger.info("Product master created successfully")
                try:
                    # Click SAVE
                    save_button = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'SAVE')]"))
                    )
                    self.safe_click(save_button, "Save button")
                    time.sleep(2)

                    # Check for error modal popup after saving
                    try:
                        error_message_element = WebDriverWait(self.driver, 5).until(
                            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'modal')]//p"))
                        )
                        error_text = error_message_element.text
                        allure.attach(self.driver.get_screenshot_as_png(), name="Error Modal Screenshot",
                                      attachment_type=allure.attachment_type.PNG)
                        raise Exception(f"Error popup appeared after saving: {error_text}")

                    except TimeoutException:
                        # No error popup appeared
                        pass

                    # Normal success screenshot
                    allure.attach(self.driver.get_screenshot_as_png(), name="Product_Created",
                                  attachment_type=allure.attachment_type.PNG)
                    logger.info("Product master created successfully.")

                except Exception as e:
                    allure.attach(self.driver.get_screenshot_as_png(), name="Unexpected_Error",
                                  attachment_type=allure.attachment_type.PNG)


        except ProductMasterCreationError:
            # Re-raise our custom exceptions
            raise

        except (NoSuchElementException, ElementNotInteractableException) as e:
            logger.error(f"Element interaction error during product creation: {e}")
            allure.attach(self.driver.get_screenshot_as_png(), name="product_creation_element_error",
                          attachment_type=allure.attachment_type.PNG)
            raise ProductMasterCreationError(f"Failed to create product master due to element interaction error: {e}")

        except TimeoutException as e:
            logger.error(f"Timeout error during product creation: {e}")
            allure.attach(self.driver.get_screenshot_as_png(), name="product_creation_timeout",
                          attachment_type=allure.attachment_type.PNG)
            raise ProductMasterCreationError(f"Failed to create product master due to timeout: {e}")

        except WebDriverException as e:
            logger.error(f"WebDriver error during product creation: {e}")
            allure.attach(self.driver.get_screenshot_as_png(), name="product_creation_webdriver_error",
                          attachment_type=allure.attachment_type.PNG)
            raise ProductMasterCreationError(f"Failed to create product master due to WebDriver error: {e}")

        except Exception as e:
            logger.error(f"Unexpected error during product creation: {e}")
            allure.attach(self.driver.get_screenshot_as_png(), name="product_creation_unexpected_error",
                          attachment_type=allure.attachment_type.PNG)
            raise ProductMasterCreationError(f"Failed to create product master due to unexpected error: {e}")
























# Functions call
# user Authentication
    @allure.feature("User Authentication")
    @allure.story("Login Functionality")
    @pytest.hookimpl(hookwrapper=True)
    def test_login_functionality(self):
        """Test login functionality with valid credentials."""
        try:
            self.login(
                TEST_CONFIG["username"],
                TEST_CONFIG["password"],
                TEST_CONFIG["url"]
            )
            logger.info("Login test passed successfully")
        except LoginFailedError as e:
            pytest.fail(f"Login test failed: {e}")

    @allure.feature("Product Management")
    @allure.story("Product Master Creation")
    @pytest.hookimpl(hookwrapper=True)
    def test_product_master_creation(self):
        """Test complete product master creation flow."""
        try:
            # First login
            self.login(
                TEST_CONFIG["username"],
                TEST_CONFIG["password"],
                TEST_CONFIG["url"]
            )

            # Then create product master
            product_data = TEST_CONFIG["product_data"]
            self.create_product_master(
                product_data["product_item"],
                product_data["HS_code"],
                product_data["unit"],
                product_data["item_type"],
                product_data["description"],
                product_data["category"],
                product_data["short_name"],
                product_data["purchase_price"],
                product_data["sales_price"],
                product_data["alt_unit"],
                product_data["conversion_factor"],
                product_data["barcode_map"],
                product_data["barcode_unit"]
            )

            logger.info("Product master creation test passed successfully")

        except (LoginFailedError, ProductMasterCreationError) as e:
            pytest.fail(f"Product master creation test failed: {e}")

    @allure.feature("End-to-End Flow")
    @allure.story("Complete Product Flow")
    @pytest.hookimpl(hookwrapper=True)
    def test_complete_product_flow(self):
        """Test complete end-to-end product flow."""
        try:
            # Login
            self.login(
                TEST_CONFIG["username"],
                TEST_CONFIG["password"],
                TEST_CONFIG["url"]
            )

            # Create product master
            product_data = TEST_CONFIG["product_data"]
            self.create_product_master(
                product_data["product_item"],
                product_data["HS_code"],
                product_data["unit"],
                product_data["item_type"],
                product_data["description"],
                product_data["category"],
                product_data["short_name"],
                product_data["purchase_price"],
                product_data["sales_price"],
                product_data["alt_unit"],
                product_data["conversion_factor"],
                product_data["barcode_map"],
                product_data["barcode_unit"]
            )

            # Additional verification or flow steps can be added here
            logger.info("Complete product flow test passed successfully")

        except (LoginFailedError, ProductMasterCreationError) as e:
            pytest.fail(f"Complete product flow test failed: {e}")


# Additional standalone test functions (if needed)
@allure.feature("Smoke Tests")
@allure.story("Basic Functionality")
@pytest.hookimpl(hookwrapper=True)
def test_webdriver_initialization():
    """Test WebDriver can be initialized without errors."""
    driver = None
    try:
        driver = webdriver.Chrome()
        logger.info("WebDriver initialization test passed")
        assert driver is not None
    except WebDriverException as e:

        pytest.fail(f"WebDriver initialization failed: {e}")
    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    # For running directly (not via pytest)
    test_instance = TestProductFlow()
    test_instance.setup_method()
    try:
        test_instance.test_complete_product_flow()
        print("✅ All tests passed when run directly")
    except Exception as e:
        print(f"❌ Test failed: {e}")
    finally:
        test_instance.teardown_method()
