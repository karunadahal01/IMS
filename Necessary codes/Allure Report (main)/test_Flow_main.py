#import pytest
import allure
import time
import logging
import random
import string
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


#--------------------------------------------------------
# Logging setup
logging.basicConfig(level=logging.INFO, format='%(pastime)s - %(levelness)s - %(message)s')
logger = logging.getLogger(__name__)


#################################################################################################
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


class NavigationError(Exception):
    """Raised when navigation to a menu or page fails."""
    pass


class FormFieldNotFoundError(Exception):
    """Raised when a required form field is not found or not interactable."""
    pass


class PopupHandlingError(Exception):
    """Raised when a popup/modal cannot be handled as expected."""
    pass


class SaveInvoiceError(Exception):
    """Raised when saving the invoice fails."""
    pass


class ProductCreationError(Exception):
    """Raised when trying to create a product that already exists."""
    pass


class PurchaseNotSuccessError(Exception):
    """Raised when the purchase transaction does not complete successfully."""
    pass


class SaveSalesInvoiceError(Exception):
    """Raised when saving the sales invoice fails."""
    pass


class ListNotFoundError(Exception):
    """Raised when saving the sales invoice fails."""
    pass

#################################################################################################


# Test class
@allure.feature("Test ERP FLow Creation")
class TestERPFlowCreation:
    # def __init__(self):
    #     self.driver = None


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
                raise WebDriverInitializationError(f"Error during driver cleanup: {e}")

    def safe_click(self, element, description="element"):
        try:
            element.click()
            logger.info(f"Clicked {description} using normal click")
        except Exception as e:
            logger.warning(f"Normal click failed for {description}, trying JS click: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name=f"{description} Click Error",
                          attachment_type=allure.attachment_type.PNG)
            self.driver.execute_script("arguments[0].click();", element)
            logger.info(f"Clicked {description} using JavaScript click")


###########################################login###############################################################################-----------------------------------
    @allure.step("Login with username: {username}")
    def login(self, username, password, link):
        driver = self.driver
        driver.maximize_window()
        driver.get(link)
        logger.info(f"Navigated to: {link}")

        username_field = WebDriverWait(driver, 15).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, 'input[formcontrolname="username"]'))
        )
        username_field.clear()
        username_field.send_keys(username)
        logger.info("Entered username")

        password_field = WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR, 'input[formcontrolname="password"]'))
        )
        password_field.clear()
        password_field.send_keys(password)
        logger.info("Entered password")
        # Click the Sign-In button
        try:
            sign_in_btn = WebDriverWait(driver, 10).until(
                ec.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign In')]"))
            )
            self.safe_click(sign_in_btn, "Sign In button")
        except Exception  as e:
            logger.error(f"Sign In button not found or not clickable: {e}")
            allure.attach(driver.get_screenshot_as_png(),
                          name="Sign In Button Error",
                          attachment_type=allure.attachment_type.PNG)
            raise LoginFailedError("Sign In button not found or not clickable")
        # Wait for the page to load after login
        try:
            logout_btn = WebDriverWait(self.driver, 20).until(
                ec.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Logout']]"))
            )
            logger.info("Already Logged In popup detected")

            # Click Logout button with fallback to JavaScript click
            try:
                with allure.step("Detected 'Already Logged In' popup — logging out first"):
                    self.safe_click(logout_btn, "Logout button")
                    logger.info("Logout button clicked successfully")
            except Exception as e:
                logger.error(f"Failed to click logout button: {e}")
                allure.attach(self.driver.get_screenshot_as_png(),
                              name="Logout Button Error",
                              attachment_type=allure.attachment_type.PNG)
                raise LoginFailedError(f"Could not click logout button: {e}")

            logger.info("Logout button clicked successfully")
            time.sleep(8)  # Wait for logout to complete

            # Wait for the "Sign In" button to be clickable and press Enter
            sign_in_btn = WebDriverWait(self.driver, 10).until(
                ec.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign In')]"))
            )

            # Press Enter on the "Sign In" button
            sign_in_btn.send_keys(Keys.ENTER)
            logger.info("Pressed Enter on Sign In button after logout")

        except Exception as e:
            logger.error(f"Failed to handle 'Already Logged In' popup: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Login Error",
                          attachment_type=allure.attachment_type.PNG)
            raise LoginFailedError(f"Login failed: {e}")
        time.sleep(10)  # Wait for the page to load after login



#####################################################Procudt Master Creation#############################################################-----------------------------------
    @allure.step("Creating product master for item: {product_item}")
    def product_master(self, product_item, HS_code, unit, item_type,
                       description, category, short_name, purchase_price, sales_price,
                       alt_unit, conversion_factor,
                       barcode_map, barcode_unit):
        # Wait until the menu is loaded
        wait = WebDriverWait(self.driver, 10)
        # Click on "Masters"
        try:
           with allure.step("Clicking on 'Masters' menu"):
            Master_menu = self.driver.find_element(By.LINK_TEXT, "Masters")
            Master_menu.click()
            print("Clicked on 'Masters'")
        except Exception as e:
            logger.error(f"Error clicking 'Masters': {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Masters Menu Error",
                          attachment_type=allure.attachment_type.PNG)
            raise NavigationError(f"Failed to click 'Masters': {e}")
        time.sleep(5)
        # Hover over "inventory_info"
        try:
            inventory_info = wait.until(ec.presence_of_element_located((By.LINK_TEXT, "Inventory Info")))
            ActionChains(self.driver).move_to_element(inventory_info).perform()
            time.sleep(5)
        except Exception as e:

            logger.error(f"Error hovering over 'Inventory Info': {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Inventory Info Hover Error",
                          attachment_type=allure.attachment_type.PNG)
            raise NavigationError(f"Failed to hover over 'Inventory Info': {e}")

        # Wait for "Product Master" to be visible and click it
        try:
            with allure.step("Waiting for 'Product Master' to be visible and clicking it"):
               product_master = wait.until(ec.visibility_of_element_located((By.LINK_TEXT, "Product Master")))
               product_master.click()
               print("Clicked 'Product Master'")
               time.sleep(5)
        except Exception as e:
            logger.error(f"Error clicking 'Product Master': {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Product Master Click Error",
                          attachment_type=allure.attachment_type.PNG)
            raise NavigationError(f"Failed to click 'Product Master': {e}")
        # Click on "Add Product" button
        try:
            with allure.step("Clicking on 'Add Product' button"):
                add_product_btn = wait.until(ec.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add Product')]")))
                self.safe_click(add_product_btn, "Add Product button")
                time.sleep(10)
        except Exception as e:
            logger.error(f"Error clicking 'Add Product' button: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Add Product Button Error",
                          attachment_type=allure.attachment_type.PNG)
            raise NavigationError(f"Failed to click 'Add Product': {e}")


        # Click the "Add Product" label

        try:
            with allure.step("Clicking 'Add Product' label"):
                wait = WebDriverWait(self.driver, 10)
                add_product = wait.until(ec.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'Add Product')]")))
                # Click the "Add Product" label
                add_product.click()
                time.sleep(8)

        except Exception as e:
            logger.error(f"Error clicking 'Add Product' label: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Add Product Label Error",
                          attachment_type=allure.attachment_type.PNG)
            raise NavigationError(f"Failed to click 'Add Product' label: {e}")
        # Zoom out screen
        self.driver.execute_script("document.body.style.zoom='80%'")
        time.sleep(3)

        # Click on the Item Group input field
        try:
            with allure.step("Clicking on Item Group input field"):
                item_group_input = wait.until(
                    ec.element_to_be_clickable((By.XPATH, "//input[@placeholder='-- Press Enter For Item Group --']")))
                item_group_input.click()
                time.sleep(5)
                # Press Enter on the Item Group field
                item_group_input.send_keys(Keys.ENTER)
                time.sleep(5)
        except Exception as e:
            logger.error(f"Error clicking Item Group input field: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Item Group Input Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Failed to click Item Group input field: {e}")
        wait = WebDriverWait(self.driver, 5)

        # Find and click the main group input field
        try:
            with allure.step("Clicking on main group input field"):
                main_group_input = wait.until(
                    ec.element_to_be_clickable((By.XPATH, "//ng-select//input[@type='text']")))
                main_group_input.click()
                # Send Enter key to trigger dropdown
                main_group_input.send_keys(Keys.ENTER)
                # Send Enter again to select the first dropdown option
                main_group_input.send_keys(Keys.ENTER)
                main_group_input.send_keys(Keys.ENTER)

                time.sleep(8)

                ok_button = wait.until(
                    ec.element_to_be_clickable((By.XPATH, "//button[.//span[normalize-space()='Ok']]")))
                ok_button.click()
        except Exception as e:
            logger.error(f"Error clicking main group input field: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Main Group Input Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Failed to click main group input field: {e}")

        # Find the input by placeholder and enter item name

        try:
            with allure.step("Entering product item name"):
                # Find the input by placeholder and enter item name
                item_name_input = wait.until(
                    ec.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter Item Name']")))
                item_name_input.clear()
                item_name_input.send_keys(product_item)
                item_name_input.send_keys(Keys.ENTER)
        except Exception as e:
            logger.error(f"Error entering product item name: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Item Name Input Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Failed to enter product item name: {e}")

        # Press Tab from keyboard
        self.driver.switch_to.active_element.send_keys(Keys.TAB)
        time.sleep(5)

        # Enter HSC code
        try:
            with allure.step("Entering HSC code"):
                self.driver.switch_to.active_element.send_keys(HS_code , Keys.TAB)
        except Exception as e:
            logger.error(f"Error entering HSC code: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="HSC Code Input Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Failed to enter HSC code: {e}")

        # Click on vatable check box
        try:
            with allure.step("Clicking on vatable checkbox"):
                wait = WebDriverWait(self.driver, 10)
                checkbox = wait.until(ec.element_to_be_clickable(
                    (By.XPATH, "//input[@type='checkbox' and contains(@class, 'ng-pristine')]")))
                checkbox.click()
                time.sleep(5)

                # press TAB
                self.driver.switch_to.active_element.send_keys(Keys.TAB)
        except Exception as e:
            logger.error(f"Error clicking vatable checkbox: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Vatable Checkbox Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Failed to click vatable checkbox: {e}")

        # To select Unit
        try:
            with allure.step("Selecting unit"):
                self.driver.switch_to.active_element.send_keys(unit, Keys.TAB)
                time.sleep(5)
        except Exception as e:
            logger.error(f"Error selecting unit: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Unit Selection Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Failed to select unit: {e}")

        # To select item type
        try:
            with allure.step("Selecting item type"):
                self.driver.switch_to.active_element.send_keys(item_type, Keys.TAB)
                time.sleep(5)
        except Exception as e:
            logger.error(f"Error selecting item type: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Item Type Selection Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Failed to select item type: {e}")

        # Description
        try:
            with allure.step("Entering description"):
                self.driver.switch_to.active_element.send_keys(Keys.TAB)
                self.driver.switch_to.active_element.send_keys(description, Keys.TAB)
                time.sleep(5)
        except Exception as e:
            logger.error(f"Error entering description: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Description Input Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Failed to enter description: {e}")

        # Category
        try:
            with allure.step("Entering category"):
                self.driver.switch_to.active_element.send_keys(category, Keys.TAB)
                time.sleep(5)
        except Exception as e:
            logger.error(f"Error entering category: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Category Input Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Failed to enter category: {e}")

        # Short name
        try:
            with allure.step("Entering short name"):
                self.driver.switch_to.active_element.send_keys(short_name, Keys.TAB)
                time.sleep(5)
        except Exception as e:
            logger.error(f"Error entering short name: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Short Name Input Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Failed to enter short name: {e}")

        # Purchase price
        try:
            with allure.step("Entering purchase price"):
                price_input = wait.until(ec.element_to_be_clickable(
                    (By.XPATH, "//input[@type='number' and @placeholder='Enter Purchase Price']")))
                price_input.clear()
                price_input.send_keys(purchase_price)
                time.sleep(10)
        except Exception as e:
            logger.error(f"Error entering purchase price: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Purchase Price Input Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Failed to enter purchase price: {e}")

        # Sales price
        try:
            with allure.step("Entering sales price"):
                number_input = wait.until(
                    ec.element_to_be_clickable((By.XPATH, "//input[@type='number' and @placeholder='0']")))
                number_input.clear()
                number_input.send_keys(sales_price)
                time.sleep(10)
        except Exception as e:
            logger.error(f"Error entering sales price: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Sales Price Input Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Failed to enter sales price: {e}")

        #Alternate Unit
        try:
           with allure.step("Navigating to Alternate Unit tab"):
            alternate_unit_tab = wait.until(ec.element_to_be_clickable(
                (By.XPATH, "//div[@class='mat-tab-label-content' and normalize-space()='Alternate Unit']")))
            alternate_unit_tab.click()
            time.sleep(8)

        except Exception as e:
            logger.error(f"Error clicking Alternate Unit tab: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Alternate Unit Tab Error",
                          attachment_type=allure.attachment_type.PNG)
            raise NavigationError(f"Failed to click Alternate Unit tab: {e}")

        # Click on "Add Alternate Unit" button
        try:
            with allure.step("Clicking on 'Add Alternate Unit' button"):
              # Select unit: gm
              select_element = wait.until(ec.element_to_be_clickable((By.XPATH, "//select[contains(@class, 'ng-pristine')]")))
              select_element.click()
              self.driver.switch_to.active_element.send_keys(alt_unit, Keys.TAB)
              print("Unit selected.")

        except Exception as e:
            logger.error(f"Error clicking 'Add Alternate Unit' button: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Add Alternate Unit Button Error",
                          attachment_type=allure.attachment_type.PNG)
            raise NavigationError(f"Failed to click 'Add Alternate Unit': {e}")

        # Enter conversion factor
        try:
            with allure.step("Entering conversion factor"):
                input_field = wait.until(
                    ec.element_to_be_clickable((By.XPATH, "//input[@type='number' and contains(@class, 'ng-valid')]")))
                input_field.clear()
                input_field.send_keys(conversion_factor)
                time.sleep(5)
        except Exception as e:
            logger.error(f"Error entering conversion factor: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Conversion Factor Input Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Failed to enter conversion factor: {e}")

        # Click on "Add Barcode" mapping tab
        try:
            with allure.step("Clicking on 'Add Barcode' button"):
                # Barcode Mapping tab
                barcode_mapping = wait.until(ec.element_to_be_clickable(
                    (By.XPATH, "//div[@class='mat-tab-label-content' and normalize-space()='Barcode Mapping']")))
                barcode_mapping.click()
                time.sleep(8)
        except Exception as e:
            logger.error(f"Error clicking 'Add Barcode' button: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Add Barcode Button Error",
                          attachment_type=allure.attachment_type.PNG)
            raise NavigationError(f"Failed to click 'Add Barcode': {e}")

        # Enter barcode
        try:
            with allure.step("Entering barcode"):
                barcode_input = wait.until(
                    ec.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter Bar Code']")))
                barcode_input.clear()
                barcode_input.send_keys(barcode_map)
                barcode_input.click()
                time.sleep(5)
                self.driver.switch_to.active_element.send_keys(Keys.TAB)
                time.sleep(5)

                select_element = self.driver.find_element(By.CSS_SELECTOR, 'div.col-2.p-0 select')
                select_element.click()
                self.driver.switch_to.active_element.send_keys(barcode_unit, Keys.TAB)
                time.sleep(5)

        except Exception as e:
            logger.error(f"Error entering barcode: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Barcode Input Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Failed to enter barcode: {e}")

        # Click on "Map" button
        try:
            with allure.step("Clicking on 'Map' button"):
                wait = WebDriverWait(self.driver, 10)
                map_button = wait.until(ec.element_to_be_clickable((By.ID, "map")))
                map_button.click()
                time.sleep(10)
        except Exception as e:
            logger.error(f"Error clicking 'Map' button: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Map Button Error",
                          attachment_type=allure.attachment_type.PNG)
            raise NavigationError(f"Failed to click 'Map': {e}")

        # Click on "Save" button
        try:
            with allure.step("Clicking on 'Save' button"):
                save_button = self.driver.find_element(By.XPATH, "//button[contains(text(),'SAVE')]")
                save_button.click()
                time.sleep(10)
        except Exception as e:
            logger.error(f"Error clicking 'Save' button: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Save Button Error",
                          attachment_type=allure.attachment_type.PNG)
            raise NavigationError(f"Failed to click 'Save': {e}")
        time.sleep(4)
        # Press enter to handle alert of "Do you want to add another product?"
        try:
           with allure.step("Handling 'Do you wanna add another product?' alert"):
                body = self.driver.find_element(By.TAG_NAME, "body")
                body.send_keys(Keys.ENTER)
                time.sleep(10)
        except Exception  as e:
            logger.error(f"Error handling 'Do you wanna add another product?' alert: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Add Another Product Alert Error",
                          attachment_type=allure.attachment_type.PNG)
            raise PopupHandlingError(f"Failed to handle 'Add Another Product' alert: {e}")



###########################################Purchase Invoice Creation#############################################################
    def Purchase_invoice(self, barcode_purchase):
        time.sleep(5)
        # Navigation to transaction
        try:
            nav_elements = self.driver.find_elements(By.XPATH, "//a | //div[@class*='nav'] | //span[@class*='nav']")
            print(f"Found {len(nav_elements)} potential navigation elements")

            visible_nav_texts = []
            for element in nav_elements[:15]:
                try:
                    text = element.text.strip()
                    if text and len(text) > 0 and element.is_displayed():
                        visible_nav_texts.append(text)
                except WebDriverException:
                     pass

            print("Available navigation texts:")
            for text in visible_nav_texts:
                print(f"  - '{text}'")
        except Exception as e:
            print(f"Navigation debug failed: {e}")
            raise NavigationError(f"Failed to Navigate: {e}")


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
                transactions_element = WebDriverWait(self.driver, 5).until(
                    ec.element_to_be_clickable((By.XPATH, selector))
                )
                actions = ActionChains(self.driver)
                actions.move_to_element(transactions_element).click().perform()
                print(f"✓ Successfully clicked on 'Transactions' using selector {i}")
                time.sleep(2)
                break # Exit loop on success

            except Exception as e:
                    print(f"✗ Failed to click on 'Transactions' using selector {i}: {e}")
                    logger.error(f"Failed to click on 'Transactions' using selector {i}: {e}")
                    raise NavigationError (f"Failed to click on 'Transactions': {e}")


        #purchase transaction hovered
        try:
            purchase_transaction_hovered = False
            if not purchase_transaction_hovered:
                print("⚠️ Trying alternative approach for Purchase Transaction hover...")
                try:
                    all_elements = self.driver.find_elements(By.TAG_NAME, "span")
                    for element in all_elements:
                        try:
                            element_text = element.text.strip()
                            if 'Purchase Transaction' in element_text and element.is_displayed():
                                actions = ActionChains(self.driver)
                                actions.move_to_element(element).perform()
                                print(f"✓ Hovered over 'Purchase Transaction' using fallback method")
                                purchase_transaction_hovered = True
                                time.sleep(2)
                                break
                        except NavigationError:
                                        continue
                except Exception as e:
                    print(f"⚠️ Fallback method for Purchase Transaction hover failed: {e}")
                    raise NavigationError(f"Failed to hover over 'Purchase Transaction': {e}")

            if not purchase_transaction_hovered:
                raise NavigationError("Could not find or hover over 'Purchase Transaction' menu")

        except Exception as e:
            logger.error(f"Failed to hover over 'Purchase Transaction': {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Purchase Transaction Hover Error",
                          attachment_type=allure.attachment_type.PNG)
            raise NavigationError(f"Failed to hover over 'Purchase Transaction': {e}")


        # Click on Purchase Invoice
        try:
           with allure.step("Clicking on 'Purchase Invoice'"):

            purchase_invoice_clicked = False
            purchase_invoice_selectors = [
                "//*[@class='dropdown-item' and contains(text(), 'Purchase Invoice')]",
                "//*[contains(@class, 'menu-item') and contains(text(), 'Purchase Invoice')]"
            ]

            for i, selector in enumerate(purchase_invoice_selectors, 1):
                try:

                    print(f"  Trying Purchase Invoice selector {i}: {selector}")
                    purchase_invoice_element = WebDriverWait(self.driver, 8).until(
                        ec.element_to_be_clickable((By.XPATH, selector))
                    )
                    actions = ActionChains(self.driver)
                    actions.move_to_element(purchase_invoice_element).click().perform()
                    print(f"✓ Successfully clicked on 'Purchase Invoice' using selector {i}")
                    purchase_invoice_clicked = True
                    time.sleep(3)
                    break
                except Exception as e:
                    print(f"  ✗ Purchase Invoice selector {i} failed: {str(e)[:100]}...")
                    continue

            if not purchase_invoice_clicked:
                print("⚠️Trying alternative approach for Purchase Invoice...")
                try:
                    invoice_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Purchase Invoice')]")
                    print(f"Found {len(invoice_elements)} elements containing 'Purchase Invoice'")
                    for element in invoice_elements:
                        try:
                            if element.is_displayed() and element.is_enabled():
                                actions = ActionChains(self.driver)
                                actions.move_to_element(element).click().perform()
                                print(f"✓ Clicked on 'Purchase Invoice' using fallback method")
                                # purchase_invoice_clicked = True
                                time.sleep(3)
                                break
                        except NavigationError:
                            continue
                except Exception as e:
                    print(f"⚠️ Fallback method for Purchase Invoice failed: {e}")

            # print("Step 9: Manually typing in Invoice Number field...")
        except Exception as e:
            logger.error(f"Failed to click on 'Purchase Invoice': {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Purchase Invoice Click Error",
                          attachment_type=allure.attachment_type.PNG)
            raise NavigationError(f"Failed to click on 'Purchase Invoice': {e}")


        # Purchase Invoice number input
        try:
           with allure.step("Entering Purchase Invoice number"):
            random_invoice = "INV-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            print(f"Generated Invoice Number: {random_invoice}")

            try:
                invoice_field = WebDriverWait(self.driver, 10).until(
                    ec.element_to_be_clickable((By.ID, "invoiceNO"))
                )
                invoice_field.clear()
                invoice_field.send_keys(random_invoice)
                print(f"✓ Successfully entered Invoice Number: {random_invoice}")
            except Exception as e:
                print(f"⚠️ Failed to enter Invoice Number: {e}")
        except Exception  as e:
            logger.error(f"Failed to enter Invoice Number: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Invoice Number Input Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Failed to enter Invoice Number: {e}")

        # Entering Account Name
        try:
            with allure.step("Entering Account Name"):
                account_field_selectors = [
                    "//input[preceding-sibling::label[contains(text(), 'Account')] or @placeholder*='Account' or contains(@formcontrolname, 'account')]",
                    "//input[contains(@placeholder, 'Press Enter to select Account')]",
                    "//*[contains(text(), 'Press Enter to select Account')]",
                    "//input[contains(@class, 'form-control') and contains(@placeholder, 'Account')]"
                ]
                account_field = None
                for selector in account_field_selectors:
                   try:
                      account_field = WebDriverWait(self.driver, 5).until(
                        ec.element_to_be_clickable((By.XPATH, selector))
                      )
                      print(f"✓ Found Account field using selector: {selector}")
                      break
                   except FormFieldNotFoundError:
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
            logger.error(f"Failed to Open Account Name list: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Account Name list Open Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Failed to open Account Name list: {e}")

        try:
           with allure.step("Selecting first account from dropdown"):
            all_inputs = self.driver.find_elements(By.TAG_NAME, "input")
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
                except FormFieldNotFoundError:
                    continue
        except Exception as e2:
            print(f"⚠️ All methods failed to open Account dropdown: {e2}")

        print("Step 11: Selecting first account by pressing Enter again...")
        try:
         with allure.step("Selecting first account by pressing Enter again"):
          if account_field:
            account_field.send_keys(Keys.ENTER)
            print("✓ Successfully pressed Enter again to select first account")
            time.sleep(2)
          else:
            focused_element = self.driver.switch_to.active_element
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
                focused_element = self.driver.switch_to.active_element
                focused_element.send_keys(Keys.ARROW_DOWN)
                time.sleep(0.5)
                focused_element.send_keys(Keys.ENTER)
                print("✓ Successfully selected first account using Arrow Down + Enter on focused element")
          except Exception as e2:
            print(f"⚠️ All methods failed: {e2}")
            try:
               with allure.step("Last resort: Trying to click on first account directly"):
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
                        first_account = WebDriverWait(self.driver, 3).until(
                            ec.element_to_be_clickable((By.XPATH, selector))
                        )
                        first_account.click()
                        print(f"✓ Successfully clicked on first account using selector: {selector}")
                        break
                    except FormFieldNotFoundError:
                        continue
            except Exception as e3:
                print(f"⚠️ All methods failed to select first account: {e3}")
        # adding Remarks
        try:
            with allure.step("Entering remarks for Purchase Invoice"):
              remarks_field = WebDriverWait(self.driver, 5).until(
                  ec.element_to_be_clickable((By.ID, "remarksid"))
              )
              remarks_field.clear()
              remarks_field.send_keys("This is an automated remark for PI.")
              time.sleep(5)
              print("✅ Remarks entered successfully.")
        except Exception as e:
            logger.error(f"Failed to enter remarks: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Remarks Input Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Failed to enter remarks: {e}")

        # Adding Barcode Purchase
        try:
           with allure.step("Adding Barcode Purchase"):
            barcode_input = self.driver.find_element(By.ID, "barcodeField")
            barcode_input.clear()
            barcode_input.send_keys(barcode_purchase)
            barcode_input.send_keys(Keys.ENTER)
        except Exception  as e:
            logger.error(f"Failed to enter Barcode Purchase: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Barcode Purchase Input Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Failed to enter Barcode Purchase: {e}")

        # generating random quantity
        try:
            with allure.step("Generating random quantity"):
                quantity = random.randint(80, 200)
                print(f"Generated quantity: {quantity}")

                xpaths = [
                    "//table//tr//td[position()=9]//input",
                    "//input[contains(@name, 'quantity') or contains(@name, 'Quantity')]",
                    "//input[contains(@id, 'quantity') or contains(@id, 'Quantity')]",
                    "//td[contains(@class, 'quantity')]//input",
                    "//table//tbody//tr[1]//td[9]//input",
                ]

                # quantity_field = None
                for xpath in xpaths:
                    try:
                       with allure.step(f"Trying XPath: {xpath}"):
                        quantity_field = WebDriverWait(self.driver, 5).until(
                            ec.element_to_be_clickable((By.XPATH, xpath))
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
        except Exception as e:
            logger.error(f"Failed to enter Quantity: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Quantity Input Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Failed to enter Quantity: {e}")

        # Discount is added here
        try:
            with allure.step("Adding Discount"):
                discount = random.randint(1, 50)
                print(f"Generated discount: {discount}%")
                try:
                    discount_field = WebDriverWait(self.driver, 5).until(
                        ec.element_to_be_clickable((By.ID, "INDDISCOUNTRATE0"))
                    )
                    discount_field.clear()
                    discount_field.send_keys(str(discount))
                    time.sleep(2)
                    print("✅ Discount entered.")
                except Exception as e:
                    print(f"❌ Discount input not found: {e}")

                # --- Discount (Dis%) 1 ---
                discount = random.randint(1, 50)
                try:
                    discount_field = WebDriverWait(self.driver, 5).until(
                        ec.element_to_be_clickable((By.ID, "INDDISCOUNTRATE1"))
                    )
                    discount_field.clear()
                    discount_field.send_keys(str(discount))
                    time.sleep(2)
                    print("✅ Discount entered.")
                except Exception as e:
                    print(f"❌ Discount input not found: {e}")
        except Exception as e:
            logger.error(f"Failed to add Discount: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Discount Input Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Failed to add Discount: {e}")

        # Click on Save button
        try:
            with allure.step("Clicking on 'Save' button"):
                wait = WebDriverWait(self.driver, 10)
                save_button = wait.until(ec.element_to_be_clickable(
                    (By.XPATH, "//button[contains(text(), 'SAVE') and contains(@class, 'btn-info')]")))
                save_button.click()
        except Exception as e:
            logger.error(f"Failed to click on 'Save' button: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Save Button Click Error",
                          attachment_type=allure.attachment_type.PNG)
            raise PurchaseNotSuccessError(f"Failed to click on 'Save': {e}")

        #  seeing Alert shown or not while clicking save button
        try:
          with allure.step("Checking for alert after clicking 'Save' button"):
            WebDriverWait(self.driver, 5).until(ec.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()
            print("Alert accepted successfully.")
        except Exception as e:
            logger.error(f"Failed to handle alert after clicking 'Save' button: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Alert Handling Error",
                          attachment_type=allure.attachment_type.PNG)
            raise PopupHandlingError(f"Failed to handle alert after clicking 'Save': {e}")

        # Cancel the print invoice bye Esc button
        try:
           with allure.step("Cancelling print invoice"):
             time.sleep(10)
             pyautogui.press('esc')
             time.sleep(5)
        except Exception  as e:
            logger.error(f"Failed to cancel print invoice: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Print Invoice Cancel Error",
                          attachment_type=allure.attachment_type.PNG)
            raise PopupHandlingError(f"Failed to cancel print invoice: {e}")

        # View invoice
        try:
            with allure.step("Viewing invoice"):
                view_button = wait.until(ec.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'VIEW')]")))
                view_button.click()
                time.sleep(2)
        except Exception as e:
            logger.error(f"Failed to click on 'View Invoice' button: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="View Invoice Button Click Error",
                          attachment_type=allure.attachment_type.PNG)
            raise NavigationError(f"Failed to click on 'View Invoice': {e}")

        # press enter to select invoice
        try:
           with allure.step("Pressing Enter to select invoice"):
               actions = ActionChains(self.driver)
               actions.send_keys(Keys.ENTER).perform()
               time.sleep(3)
        except Exception  as e:
            logger.error(f"Failed to press Enter to select invoice: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                            name="Select Invoice Error",
                            attachment_type=allure.attachment_type.PNG)
            raise ListNotFoundError(f"Failed to press Enter to select invoice: {e}")

        # Reset the form
        try:
           with allure.step("Resetting the form"):
               reset_btn = wait.until(ec.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'RESET')]")))
               reset_btn.click()
        except Exception  as e:
            logger.error(f"Failed to click on 'Reset' button: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Reset Button Click Error",
                          attachment_type=allure.attachment_type.PNG)
            raise NavigationError(f"Failed to click on 'Reset': {e}")
        time.sleep(3)

        # To click on alert of reset
        try:
            with allure.step("Handling reset confirmation alert"):

                wait.until(ec.alert_is_present())
                alert = self.driver.switch_to.alert
                alert.accept()
                time.sleep(5)
        except Exception as e:
            logger.error(f"Failed to handle reset confirmation alert: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Reset Confirmation Alert Error",
                          attachment_type=allure.attachment_type.PNG)
            raise PopupHandlingError(f"Failed to handle reset confirmation alert: {e}")



        # CLick on back button to come in dashboard
        try:
            with allure.step("Clicking on 'Back' button"):
                back_btn = wait.until(ec.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'BACK')]")))
                back_btn.click()
                time.sleep(5)

        except Exception as e:
            logger.error(f"Failed to click on 'Back' button: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Back Button Click Error",
                          attachment_type=allure.attachment_type.PNG)
            raise NavigationError(f"Failed to click on 'Back': {e}")


##################################sales tax invoice creation######################################################################################

    def sales_tax_invoice(self,barcode_sales):
        # Wait until the menu is loaded
        wait = WebDriverWait(self.driver, 10)

        # Click on "Transactions"
        try:
           with allure.step("Clicking on 'Transactions' menu"):
            transaction_menu = self.driver.find_element(By.LINK_TEXT, "Transactions")
            transaction_menu.click()
            print("Clicked on 'Transactions'")
        except Exception as e:
            print("Error clicking 'Transactions':", e)
            logger.error(f"Error clicking 'Transactions': {e}")
            raise NavigationError(f"Failed to click on 'Transactions': {e}")
        time.sleep(10)

        # Hover over "Sales Transaction"
        try:
           with allure.step("Hovering over 'Sales Transaction'"):
             sales_transaction = wait.until(ec.presence_of_element_located((By.LINK_TEXT, "Sales Transaction")))
             ActionChains(self.driver).move_to_element(sales_transaction).perform()
             time.sleep(5)
        except Exception  as e:
            logger.error(f"Error hovering over 'Sales Transaction': {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Sales Transaction Hover Error",
                          attachment_type=allure.attachment_type.PNG)
            raise NavigationError(f"Failed to hover over 'Sales Transaction': {e}")

        # Wait for "Sales Tax Invoice" to be visible and click it
        try:
           with allure.step("Clicking on 'Sales Tax Invoice'"):
               sales_tax_invoice_link = wait.until(
                   ec.visibility_of_element_located((By.LINK_TEXT, "Sales Tax Invoice")))
               sales_tax_invoice_link.click()
               print("Clicked 'Sales Tax Invoice'")
               time.sleep(5)
        except Exception as e:
            logger.error(f"Error clicking 'Sales Tax Invoice': {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Sales Tax Invoice Click Error",
                          attachment_type=allure.attachment_type.PNG)
            raise NavigationError(f"Failed to click on 'Sales Tax Invoice': {e}")

        # Generate random reference Number
        try:
           with allure.step("Generating random reference number"):
               # Generate random refno
               def generate_random_refno(length=8):
                   letters_and_digits = string.ascii_letters + string.digits
                   # return ''.join(random.choice(letters_and_digits) for i in range(length))
                   return ''.join(random.choices(letters_and_digits, k=length))

               random_refno = generate_random_refno()
               print(f"Generated Refno: {random_refno}")

               refno_input = self.driver.find_element(By.ID, "refnoInput")
               refno_input.clear()
               refno_input.send_keys(random_refno)
               time.sleep(3)
        except Exception  as e:
            logger.error(f"Error generating random reference number: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Reference Number Generation Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Failed to generate random reference number: {e}")

        # Enter customer on Customer input field
        try:
           with allure.step("Entering customer in Customer input field"):
               customer_input = wait.until(ec.element_to_be_clickable((By.ID, "customerselectid")))
               customer_input.click()
               customer_input.send_keys(Keys.ENTER)
               time.sleep(5)
               # Press ENTER on body to confirm selection
               body = self.driver.find_element(By.TAG_NAME, "body")
               body.send_keys(Keys.ENTER)
               time.sleep(10)

        except Exception  as e:
            logger.error(f"Error entering customer in Customer input field: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Customer Input Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Failed to enter customer in Customer input field: {e}")



        # Enter Remarks
        try:
           with allure.step("Entering remarks for Sales Tax Invoice"):
               remarks_field = wait.until(ec.element_to_be_clickable((By.ID, "remarksid")))
               remarks_field.clear()
               remarks_field.send_keys("This is an automated remark for STI.")
               time.sleep(5)
               print("✅ Remarks entered successfully.")
        except Exception as e:
            logger.error(f"Failed to enter remarks: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Remarks Input Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Failed to enter remarks: {e}")

        # --- Barcode Section ---
        try:
              with allure.step("Entering barcode for Sales Tax Invoice"):
                 barcode_input = self.driver.find_element(By.ID, "barcodeField")
                 barcode_input.clear()
                 barcode_input.send_keys(barcode_sales)
                 barcode_input.send_keys(Keys.ENTER)
        except Exception as e:
                logger.error(f"Failed to enter Barcode Sales: {e}")
                allure.attach(self.driver.get_screenshot_as_png(),
                              name="Barcode Sales Input Error",
                              attachment_type=allure.attachment_type.PNG)
                raise FormFieldNotFoundError(f"Failed to enter Barcode Sales: {e}")

        # --- Quantity Section ---

        try:
            with allure.step("Generating random quantity for Sales Tax Invoice"):
                quantity = random.randint(10, 80)
                print(f"Generated quantity: {quantity}")

                xpaths = [
                    "//table//tr//td[position()=9]//input",
                    "//input[contains(@name, 'quantity') or contains(@name, 'Quantity')]",
                    "//input[contains(@id, 'quantity') or contains(@id, 'Quantity')]",
                    "//td[contains(@class, 'quantity')]//input",
                    "//table//tbody//tr[1]//td[9]//input",
                ]

                # quantity_field = None
                for xpath in xpaths:
                    try:
                        quantity_field = WebDriverWait(self.driver, 5).until(
                            ec.element_to_be_clickable((By.XPATH, xpath))
                        )
                        quantity_field.clear()
                        quantity_field.send_keys(str(quantity) + Keys.ENTER)
                        print("✅ Quantity entered and Enter key pressed.")
                        time.sleep(2)
                        break
                    except Exception as e:
                        print(f"⚠ Failed with XPath: {xpath} -> {e}")
        except Exception as e:
            logger.error(f"Failed to enter Quantity: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Quantity Input Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Failed to enter Quantity: {e}")

        #CLick on show details
        try:
            with allure.step("Clicking on 'Show Details'"):
                body = self.driver.find_element(By.TAG_NAME, 'body')
                body.send_keys(Keys.F1)
                time.sleep(5)

        except Exception as e:
            logger.error(f"Failed to click on 'Show Details': {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Show Details Click Error",
                          attachment_type=allure.attachment_type.PNG)
            raise NavigationError(f"Failed to click on 'Show Details': {e}")

        # Adding Flat Discount
        try:
            with allure.step("Adding Flat Discount"):
                # Flat Discount
                flat_discount = random.randint(1, 50)
                print(f"Generated Flat Discount: {flat_discount}%")

                input_field = self.driver.find_element(By.ID, "flatDis1")
                input_field.clear()
                input_field.send_keys(str(flat_discount) + Keys.ENTER)
                time.sleep(3)
                try:
                  # AFTER button
                  after_button = wait.until(
                      ec.element_to_be_clickable((By.XPATH, "//button[text()='AFTER']"))
                  )
                  after_button.click()
                except Exception  as e:
                    logger.error(f"Failed to click on 'AFTER' button: {e}")
                    allure.attach(self.driver.get_screenshot_as_png(),
                                    name="After Button Click Error",
                                    attachment_type=allure.attachment_type.PNG)
                    raise NavigationError(f"Failed to click on 'AFTER': {e}")

        except Exception as e:
            logger.error(f"Failed to add Flat Discount: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Flat Discount Input Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Failed to add Flat Discount: {e}")

        # click on save button
        try:
            with allure.step("Clicking on 'Save' button"):
                time.sleep(5)
                save_button = wait.until(ec.element_to_be_clickable(
                    (By.XPATH, "//button[contains(text(), 'SAVE') and contains(@class, 'btn-info')]")))
                save_button.click()
                time.sleep(5)
        except Exception as e:
            logger.error(f"Failed to click on 'Save' button: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Save Button Click Error",
                          attachment_type=allure.attachment_type.PNG)
            raise PurchaseNotSuccessError(f"Failed to click on 'Save': {e}")

       ######### For payment ###############
        # Balance Amount
        try:
          with allure.step("Clicking on 'Balance Amount' button"):
             balance_amount_button = wait.until(ec.element_to_be_clickable(
                  (By.XPATH, "//button[contains(text(), 'Balance Amount') and contains(@class, 'btn-info')]")))
             balance_amount_button.click()
             time.sleep(5)
        except Exception as e:
            logger.error(f"Failed to click on 'Balance Amount' button: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Balance Amount Button Click Error",
                          attachment_type=allure.attachment_type.PNG)
            raise NavigationError(f"Failed to click on 'Balance Amount': {e}")

        # Add button
        try:
            add_button = wait.until(ec.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Add') and contains(@class, 'btn-info')]")))
            add_button.click()
            time.sleep(5)
        except Exception as e:
            logger.error(f"Failed to click on 'Add' button: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Add Button Click Error",
                          attachment_type=allure.attachment_type.PNG)
            raise NavigationError(f"Failed to click on 'Add': {e}")

        # CLICK to End key to Save the payment
        try:
            with allure.step("Pressing 'End' key to save payment"):
                body = self.driver.find_element(By.TAG_NAME, 'body')
                body.send_keys(Keys.END)
                time.sleep(10)
        except Exception as e:
            logger.error(f"Failed to press 'End' key: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="End Key Press Error",
                          attachment_type=allure.attachment_type.PNG)
            raise PopupHandlingError(f"Failed to press 'End' key: {e}")

        # View invoice
        try:
            with allure.step("Viewing invoice"):
                # View Voucher
                view_button = wait.until(ec.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'VIEW')]")))
                view_button.click()
                time.sleep(2)
                # Press Enter to select invoice
                try:
                  with allure.step("Pressing Enter to select invoice"):
                   actions = ActionChains(self.driver)
                   actions.send_keys(Keys.ENTER).perform()
                   time.sleep(5)
                except Exception    as e:
                    logger.error(f"Failed to press Enter to select invoice: {e}")
                    allure.attach(self.driver.get_screenshot_as_png(),
                                  name="Select Invoice Error",
                                  attachment_type=allure.attachment_type.PNG)
                    raise ListNotFoundError(f"Failed to press Enter to select invoice: {e}")
        except Exception as e:
            logger.error(f"Failed to click on 'View Invoice' button: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="View Invoice Button Click Error",
                          attachment_type=allure.attachment_type.PNG)
            raise NavigationError(f"Failed to click on 'View Invoice': {e}")


        # Reset the form
        try:
            with allure.step("Resetting the form"):
                # Reset button
                reset_btn = wait.until(ec.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'RESET')]")))
                reset_btn.click()
                time.sleep(5)
        except Exception as e:
            logger.error(f"Failed to click on 'Reset' button: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Reset Button Click Error",
                          attachment_type=allure.attachment_type.PNG)
            raise NavigationError(f"Failed to click on 'Reset': {e}")


        # To click on alert of reset
        try:
            with allure.step("Handling reset confirmation alert"):
                wait.until(ec.alert_is_present())
                alert = self.driver.switch_to.alert
                alert.accept()
                time.sleep(5)
        except Exception as e:
            logger.error(f"Failed to handle reset confirmation alert: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Reset Confirmation Alert Error",
                          attachment_type=allure.attachment_type.PNG)
            raise PopupHandlingError(f"Failed to handle reset confirmation alert: {e}")

        # Click on back button to come in dashboard
        try:
            with allure.step("Clicking on 'Back' button"):
                back_btn = wait.until(ec.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'BACK')]")))
                back_btn.click()
        except Exception as e:
            logger.error(f"Failed to click on 'Back' button: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Back Button Click Error",
                          attachment_type=allure.attachment_type.PNG)
            raise NavigationError(f"Failed to click on 'Back': {e}")


###################################################################Purchase return ####################################################
    def purchase_return(self, Remarks):
        # Wait until the menu is loaded
        wait = WebDriverWait(self.driver, 10)
        time.sleep(10)
        # Click on "Transactions"
        try:
           with allure.step("Clicking on 'Transactions' menu"):
               transaction_menu = self.driver.find_element(By.LINK_TEXT, "Transactions")
               transaction_menu.click()
               print("Clicked on 'Transactions'")
        except Exception as e:
            print("Error clicking 'Transactions':", e)
            logger.error(f"Error clicking 'Transactions': {e}")
            raise NavigationError(f"Failed to click on 'Transactions': {e}")

        # Hover over "Purchase Transaction"
        try:
          with allure.step("Hovering over 'Purchase Transaction'"):
              purchase_transaction = wait.until(ec.presence_of_element_located((By.LINK_TEXT, "Purchase Transaction")))
              ActionChains(self.driver).move_to_element(purchase_transaction).perform()
              time.sleep(8)
        except Exception as e:
            logger.error(f"Error hovering over 'Purchase Transaction': {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Purchase Transaction Hover Error",
                          attachment_type=allure.attachment_type.PNG)
            raise NavigationError(f"Failed to hover over 'Purchase Transaction': {e}")

        #Navigte to purchase return
        try:
            with allure.step("Clicking on 'Purchase Return'"):
                debit_note = wait.until(
                    ec.visibility_of_element_located((By.LINK_TEXT, "Debit Note (Purchase Return)")))
                debit_note.click()
                print("Clicked 'debit note'")
                time.sleep(8)
        except Exception  as e:
            logger.error(f"Error clicking 'Purchase Return': {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Purchase Return Click Error",
                          attachment_type=allure.attachment_type.PNG)
            raise NavigationError(f"Failed to click on 'Purchase Return': {e}")

        # Click on the invoiceNO input field
        try:
            with allure.step("Clicking on invoiceNO input field"):
                invoiceNO_input = self.driver.find_element(By.ID, "invoiceNO")
                self.driver.execute_script("arguments[0].removeAttribute('readonly')", invoiceNO_input)  # Remove readonly
                invoiceNO_input.click()
                invoiceNO_input.send_keys(Keys.ENTER)  # First Enter to load the dropdown

                # Wait for options to appear
                time.sleep(2)

                # Find the body element and send Enter key
                body = self.driver.find_element(By.TAG_NAME, "body")
                body.send_keys(Keys.ENTER)

                time.sleep(3)
        except Exception as e:
            logger.error(f"Failed to click on invoiceNO input field: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="InvoiceNO Input Field Click Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Failed to click on invoiceNO input field: {e}")

        # For remarks
        try:
          with allure.step("Entering remarks for Purchase Return"):
             remarks_field = WebDriverWait(self.driver, 5).until(
                 ec.element_to_be_clickable((By.ID, "remarksid"))
             )
             time.sleep(5)
             remarks_field.clear()
             remarks_field.send_keys(Remarks)
             time.sleep(5)
             print("✅ Remarks entered successfully.")

             time.sleep(5)
        except Exception    as e:
            logger.error(f"Failed to enter remarks: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Remarks Input Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Failed to enter remarks: {e}")

        # Click on SAVE button
        try:
          with allure.step("Clicking on 'Save' button"):
               save_button = self.driver.find_element(By.XPATH, "//button[contains(text(),'SAVE')]")
               save_button.click()
               time.sleep(10)
        except Exception    as e:
            logger.error(f"Failed to click on 'Save' button: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Save Button Click Error",
                          attachment_type=allure.attachment_type.PNG)
            raise PurchaseNotSuccessError(f"Failed to click on 'Save': {e}")

        # Handle alert ONLY if present
        try:
          with allure.step("Handling alert after clicking 'Save' button"):
              WebDriverWait(self.driver, 5).until(ec.alert_is_present())
              alert = self.driver.switch_to.alert
              alert.accept()
              print("Alert accepted successfully.")
        except Exception    as e:
            logger.error(f"Failed to handle alert after clicking 'Save' button: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Alert Handling Error",
                          attachment_type=allure.attachment_type.PNG)
            raise PopupHandlingError(f"Failed to handle alert after clicking 'Save': {e}")

        # Cancel the print invoice bye Esc button
        try:
          with allure.step("Cancelling print invoice"):
              time.sleep(10)
              pyautogui.press('esc')
              time.sleep(5)
        except Exception    as e:
            logger.error(f"Failed to cancel print invoice: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Print Invoice Cancel Error",
                          attachment_type=allure.attachment_type.PNG)
            raise PopupHandlingError(f"Failed to cancel print invoice: {e}")

        # Click on back button to come in dashboard
        try:
          with allure.step("Clicking on 'Back' button"):
                back_btn = wait.until(ec.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'BACK')]")))
                back_btn.click()
        except Exception    as e:
            logger.error(f"Failed to click on 'Back' button: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Back Button Click Error",
                          attachment_type=allure.attachment_type.PNG)
            raise NavigationError(f"Failed to click on 'Back': {e}")

#########################################sales return Full ######################################################
    def sales_return_full(self):
        # Wait until the menu is loaded
        wait = WebDriverWait(self.driver, 10)

        # Click on "Transactions"
        try:
            transaction_menu = self.driver.find_element(By.LINK_TEXT, "Transactions")
            transaction_menu.click()
            print("Clicked on 'Transactions'")
        except Exception as e:
            print("Error clicking 'Transactions':", e)
            logger.error(f"Error clicking 'Transactions': {e}")
            raise NavigationError(f"Failed to click on 'Transactions': {e}")

        # Hover over "Sales Transaction"
        try:
            sales_transaction = wait.until(ec.presence_of_element_located((By.LINK_TEXT, "Sales Transaction")))
            ActionChains(self.driver).move_to_element(sales_transaction).perform()
            time.sleep(5)
        except Exception as e:
            logger.error(f"Error hovering over 'Sales Transaction': {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Sales Transaction Hover Error",
                          attachment_type=allure.attachment_type.PNG)
            raise NavigationError(f"Failed to hover over 'Sales Transaction': {e}")

        # Wait for "Credit Note (Sales Return)" to be visible and click it
        try:
          with allure.step("Clicking on 'Credit Note (Sales Return)'"):
              sales_return = wait.until(ec.visibility_of_element_located((By.LINK_TEXT, "Credit Note (Sales Return)")))
              sales_return.click()
              print("Clicked 'Credit Note (Sales Return)'")
              time.sleep(5)

        except Exception as e:
            logger.error(f"Error clicking 'Credit Note (Sales Return)': {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Sales Return Click Error",
                          attachment_type=allure.attachment_type.PNG)
            raise NavigationError(f"Failed to click on 'Credit Note (Sales Return)': {e}")

        # Click on the Ref Bill No input field
        try:
            with allure.step("Clicking on Ref Bill No input field"):

                refbill_input = self.driver.find_element(By.ID, "refbill")
                self.driver.execute_script("arguments[0].removeAttribute('readonly')", refbill_input)
                refbill_input.click()
                refbill_input.send_keys(Keys.ENTER)
                time.sleep(2)


                # Find the body element and send Enter key
                body = self.driver.find_element(By.TAG_NAME, "body")
                body.send_keys(Keys.ENTER)

                time.sleep(3)
        except Exception as e:
            logger.error(f"Failed to click on Ref Bill No input field: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Ref Bill No Input Field Click Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Failed to click on Ref Bill No input field: {e}")


        # For remarks
        try:
          with allure.step("Entering remarks for Sales Return"):
              remarks_field = WebDriverWait(self.driver, 5).until(
                 ec.element_to_be_clickable((By.ID, "remarksid"))
              )
              time.sleep(5)
              remarks_field.clear()
              remarks_field.send_keys("sales Return by automation. ")
              time.sleep(5)
              print("✅ Remarks entered successfully.")
        except Exception    as e:
            logger.error(f"Failed to enter remarks: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Remarks Input Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Failed to enter remarks: {e}")
        time.sleep(5)



        # Click on SAVE button
        try:
            with allure.step("Clicking on 'Save' button"):
                save_button = self.driver.find_element(By.XPATH, "//button[contains(text(),'SAVE')]")
                save_button.click()
                time.sleep(10)

        except Exception  as e:
            logger.error(f"Failed to click on 'Save' button: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Save Button Click Error",
                          attachment_type=allure.attachment_type.PNG)
            raise PurchaseNotSuccessError(f"Failed to click on 'Save': {e}")


        # Click on back button to come in dashboard
        try:
            with allure.step("Clicking on 'Back' button"):
                back_btn = wait.until(ec.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'BACK')]")))
                back_btn.click()
        except Exception as e:
            logger.error(f"Failed to click on 'Back' button: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Back Button Click Error",
                          attachment_type=allure.attachment_type.PNG)
            raise NavigationError(f"Failed to click on 'Back': {e}")

############################################################## Sales Return partial ######################################################
    def sales_return_partial(self, return_barcode):
        # Wait until the menu is loaded
        wait = WebDriverWait(self.driver, 10)

        # Click on "Transactions"
        try:
            transaction_menu = self.driver.find_element(By.LINK_TEXT, "Transactions")
            transaction_menu.click()
            print("Clicked on 'Transactions'")

        except Exception as e:
            print("Error clicking 'Transactions':", e)
            logger.error(f"Error clicking 'Transactions': {e}")
            raise NavigationError(f"Failed to click on 'Transactions': {e}")

        # Hover over "Sales Transaction"
        try:
          with allure.step("Hovering over 'Sales Transaction'"):
                sales_transaction = wait.until(ec.presence_of_element_located((By.LINK_TEXT, "Sales Transaction")))
                ActionChains(self.driver).move_to_element(sales_transaction).perform()
                time.sleep(5)
        except Exception    as e:
            logger.error(f"Error hovering over 'Sales Transaction': {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Sales Transaction Hover Error",
                          attachment_type=allure.attachment_type.PNG)
            raise NavigationError(f"Failed to hover over 'Sales Transaction': {e}")

        # Wait for "Credit Note (Sales Return)" to be visible and click it
        try:
          with allure.step("Clicking on 'Credit Note (Sales Return)'"):
              sales_return = wait.until(ec.visibility_of_element_located((By.LINK_TEXT, "Credit Note (Sales Return)")))
              sales_return.click()
              print("Clicked 'Credit Note (Sales Return)'")
              time.sleep(5)
        except Exception    as e:
            logger.error(f"Error clicking 'Credit Note (Sales Return)': {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Sales Return Click Error",
                          attachment_type=allure.attachment_type.PNG)
            raise NavigationError(f"Failed to click on 'Credit Note (Sales Return)': {e}")

        # wait until the checkbox is present and click
        try:
            with allure.step("Clicking on checkbox"):
                checkbox = wait.until(
                    ec.element_to_be_clickable(
                        (By.XPATH, "//input[@type='checkbox' and contains(@class, 'ng-pristine')]")))
                checkbox.click()
                time.sleep(5)

        except Exception  as e:
            logger.error(f"Error clicking checkbox: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Checkbox Click Error",
                          attachment_type=allure.attachment_type.PNG)
            raise NavigationError(f"Failed to click on checkbox: {e}")


        # Click on the Ref Bill No input field
        try:
            with allure.step("Clicking on Ref Bill No input field"):
                # Click on the Ref Bill No input field
                refbill_input = self.driver.find_element(By.ID, "refbill")
                self.driver.execute_script("arguments[0].removeAttribute('readonly')", refbill_input)
                refbill_input.click()
                refbill_input.send_keys(Keys.ENTER)
                time.sleep(2)

                # Send Enter to the body
                body = self.driver.find_element(By.TAG_NAME, "body")
                body.send_keys(Keys.ENTER)

                time.sleep(3)
        except Exception as e:
            logger.error(f"Failed to click on Ref Bill No input field: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Ref Bill No Input Field Click Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Failed to click on Ref Bill No input field: {e}")

        # For remarks
        try:
          with allure.step("Entering remarks for Sales Return"):
              remarks_field = WebDriverWait(self.driver, 5).until(
                 ec.element_to_be_clickable((By.ID, "remarksid"))
              )
              time.sleep(5)
              remarks_field.clear()
              remarks_field.send_keys("Partial sales Return by automation. ")
              time.sleep(5)
              print("✅ Remarks entered successfully.")
        except Exception    as e:
            logger.error(f"Failed to enter remarks: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Remarks Input Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Failed to enter remarks: {e}")

        # ===   barcode Enter ===
        try:
           with allure.step("Entering barcode for Sales Return"):
               barcode_input = self.driver.find_element(By.ID, "barcodeField")
               barcode_input.clear()
               barcode_input.send_keys(return_barcode)
               barcode_input.send_keys(Keys.ENTER)

               quantity = random.randint(1, 20)
               print(f"Generated quantity for barcode {return_barcode}: {quantity}")

               xpaths = [
                   "//table//tr//td[position()=9]//input",
                   "//input[contains(@name, 'quantity') or contains(@name, 'Quantity')]",
                   "//input[contains(@id, 'quantity') or contains(@id, 'Quantity')]",
                   "//td[contains(@class, 'quantity')]//input",
                   "//table//tbody//tr[1]//td[9]//input",
               ]

               for xpath in xpaths:
                   try:
                       quantity_field = WebDriverWait(self.driver, 5).until(
                           ec.element_to_be_clickable((By.XPATH, xpath))
                       )
                       quantity_field.clear()
                       quantity_field.send_keys(str(quantity) + Keys.ENTER)
                       print(f"✅ Quantity entered for barcode {return_barcode}")
                       time.sleep(2)
                       break
                   except Exception as e:
                       print(f"⚠ Failed with XPath: {xpath} -> {e}")
                       logger.error(f"Failed with XPath: {xpath} -> {e}")
                       allure.attach(self.driver.get_screenshot_as_png(),
                                        name="Quantity Input Error",
                                        attachment_type=allure.attachment_type.PNG)
                       raise FormFieldNotFoundError(f"Failed to enter quantity for barcode {return_barcode}: {e}")
               else:
                   print(f"❌ Could not locate quantity input for barcode {return_barcode}")

        except Exception as e:
            logger.error(f"❌ Error in processing barcode '{return_barcode}': {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Barcode Input Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Failed to process barcode '{return_barcode}': {e}")
        time.sleep(5)

        # Click on SAVE button
        try:
          with allure.step("Clicking on 'Save' button"):
              save_button = self.driver.find_element(By.XPATH, "//button[contains(text(),'SAVE')]")
              save_button.click()
              time.sleep(10)
        except Exception    as e:
            logger.error(f"Failed to click on 'Save' button: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Save Button Click Error",
                          attachment_type=allure.attachment_type.PNG)
            raise PurchaseNotSuccessError(f"Failed to click on 'Save': {e}")

        # Click on back button
        try:
          with allure.step("Clicking on 'Back' button"):
              back_btn = wait.until(ec.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'BACK')]")))
              back_btn.click()
        except Exception as e:
            logger.error(f"Failed to click on 'Back' button: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Back Button Click Error",
                          attachment_type=allure.attachment_type.PNG)
            raise NavigationError(f"Failed to click on 'Back': {e}")





########################################################################################################################
    # Test case first ( Login)

    def test_login(self):
        allure.step("Login to the application")
        self.login("gedehim917@decodewp.com",
                   "Tebahal1!",
                   "https://velvet.webredirect.himshang.com.np/#/pages/dashboard")


# Test case second (login, Product Master)

    def test_product_master(self):
        allure.step("Creating new product item")
        self.login("gedehim917@decodewp.com",
                   "Tebahal1!",
                   "https://velvet.webredirect.himshang.com.np/#/pages/dashboard")
        self.product_master(
                       product_item="tested1",
                       HS_code="123",
                       unit="kg.",
                       item_type="Service Item",
                       description="This is description",
                       category="N/A",
                       short_name="XYZ",
                       purchase_price="120",
                       sales_price="140",
                       alt_unit="Each",
                       conversion_factor="1000",
                       barcode_map="555",
                       barcode_unit="kg.")


# Test case Third (Login,Product master, Purchase Invoice)

    def test_purchase_invoice(self):
        allure.step("PURCHASE a product item")
        self.login("gedehim917@decodewp.com",
                   "Tebahal1!",
                   "https://velvet.webredirect.himshang.com.np/#/pages/dashboard")
        self.product_master(
            product_item="Tested2",
            HS_code="123",
            unit="kg.",
            item_type="Service Item",
            description="This is description",
            category="N/A",
            short_name="XYZ",
            purchase_price="120",
            sales_price="140",
            alt_unit="Each",
            conversion_factor="1000",
            barcode_map="666",
            barcode_unit="kg.")

        self.Purchase_invoice(
                         barcode_purchase=666)

# Test case Fourth (Login,Product master, Sales Tax Invoice)

    def test_sales_tax_invoice(self):
        allure.step("Sales a product item")
        self.login("gedehim917@decodewp.com",
                   "Tebahal1!",
                   "https://velvet.webredirect.himshang.com.np/#/pages/dashboard")
        self.product_master(
            product_item="Test3",
            HS_code="123",
            unit="kg.",
            item_type="Service Item",
            description="This is description",
            category="N/A",
            short_name="XYZ",
            purchase_price="120",
            sales_price="140",
            alt_unit="Each",
            conversion_factor="1000",
            barcode_map="777",
            barcode_unit="kg.")

        self.Purchase_invoice(
                         barcode_purchase=777)

        self.sales_tax_invoice(
                        barcode_sales=777)


# Test case Fifth (Login,purchase, purchase  Return)

    def test_purchase_return(self):
        allure.step("Return a purchase invoice")
        self.login("gedehim917@decodewp.com",
                   "Tebahal1!",
                   "https://velvet.webredirect.himshang.com.np/#/pages/dashboard")

        self.purchase_return( Remarks="Testing Purchase Return by automation.")

    # Test case Sixth (Login,sales, sales  Return full)
    def test_sales_return(self):
            allure.step("sales return full")
            self.login("gedehim917@decodewp.com",
                       "Tebahal1!",
                       "https://velvet.webredirect.himshang.com.np/#/pages/dashboard")


            self.sales_tax_invoice(
                barcode_sales=777)
            self.sales_return_full( )

# Test case Sixth (Login,sales, sales  Return partial)

    def test_sales_return_Partial(self):
        allure.step("sales return partial")
        self.login("gedehim917@decodewp.com",
                   "Tebahal1!",
                   "https://velvet.webredirect.himshang.com.np/#/pages/dashboard")

        self.sales_tax_invoice(
            barcode_sales=777)
        self.sales_return_partial( return_barcode="15")



print("Keeping browser open for 30 seconds for observation...")
time.sleep(30)


