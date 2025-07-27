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
class Test_product_master:
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


