# pages/product_master_page.py

import time
import logging
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from pages.base_page import BasePage
from exceptions.custom_exceptions import NavigationError, FormFieldNotFoundError, PopupHandlingError

logger = logging.getLogger(__name__)


class ProductMasterPage(BasePage):
    """Product Master page class with product creation functionality."""

    # Locators
    MASTERS_MENU = (By.LINK_TEXT, "Masters")
    INVENTORY_INFO_MENU = (By.LINK_TEXT, "Inventory Info")
    PRODUCT_MASTER_MENU = (By.LINK_TEXT, "Product Master")
    ADD_PRODUCT_BUTTON = (By.XPATH, "//button[contains(text(), 'Add Product')]")
    ADD_PRODUCT_LABEL = (By.XPATH, "//label[contains(text(), 'Add Product')]")
    ITEM_GROUP_INPUT = (By.XPATH, "//input[@placeholder='-- Press Enter For Item Group --']")
    MAIN_GROUP_INPUT = (By.XPATH, "//ng-select//input[@type='text']")
    OK_BUTTON = (By.XPATH, "//button[.//span[normalize-space()='Ok']]")
    ITEM_NAME_INPUT = (By.XPATH, "//input[@placeholder='Enter Item Name']")
    VATABLE_CHECKBOX = (By.XPATH, "//input[@type='checkbox' and contains(@class, 'ng-pristine')]")
    PURCHASE_PRICE_INPUT = (By.XPATH, "//input[@type='number' and @placeholder='Enter Purchase Price']")
    SALES_PRICE_INPUT = (By.XPATH, "//input[@type='number' and @placeholder='0']")
    ALTERNATE_UNIT_TAB = (By.XPATH, "//div[@class='mat-tab-label-content' and normalize-space()='Alternate Unit']")
    UNIT_SELECT = (By.XPATH, "//select[contains(@class, 'ng-pristine')]")
    CONVERSION_FACTOR_INPUT = (By.XPATH, "//input[@type='number' and contains(@class, 'ng-valid')]")
    BARCODE_MAPPING_TAB = (By.XPATH, "//div[@class='mat-tab-label-content' and normalize-space()='Barcode Mapping']")
    BARCODE_INPUT = (By.XPATH, "//input[@placeholder='Enter Bar Code']")
    BARCODE_UNIT_SELECT = (By.CSS_SELECTOR, 'div.col-2.p-0 select')
    MAP_BUTTON = (By.ID, "map")
    SAVE_BUTTON = (By.XPATH, "//button[contains(text(),'SAVE')]")

    @allure.step("Creating product master for item: {product_item}")
    def create_product_master(self, product_item, HS_code, unit, item_type,
                              description, category, short_name, purchase_price, sales_price,
                              alt_unit, conversion_factor, barcode_map, barcode_unit):
        """Create a new product master."""

        # Navigate to Masters menu
        try:
            with allure.step("Clicking on 'Masters' menu"):
                Master_menu = self.driver.find_element(*self.MASTERS_MENU)
                Master_menu.click()
                print("Clicked on 'Masters'")
        except Exception as e:
            logger.error(f"Error clicking 'Masters': {e}")
            self.take_screenshot("Masters Menu Error")
            raise NavigationError(f"Failed to click 'Masters': {e}")
        time.sleep(5)

        # Hover over Inventory Info
        try:
            inventory_info = self.wait.until(ec.presence_of_element_located(self.INVENTORY_INFO_MENU))
            ActionChains(self.driver).move_to_element(inventory_info).perform()
            time.sleep(5)
        except Exception as e:
            logger.error(f"Error hovering over 'Inventory Info': {e}")
            self.take_screenshot("Inventory Info Hover Error")
            raise NavigationError(f"Failed to hover over 'Inventory Info': {e}")

        # Click Product Master
        try:
            with allure.step("Waiting for 'Product Master' to be visible and clicking it"):
                product_master = self.wait.until(ec.visibility_of_element_located(self.PRODUCT_MASTER_MENU))
                product_master.click()
                print("Clicked 'Product Master'")
                time.sleep(5)
        except Exception as e:
            logger.error(f"Error clicking 'Product Master': {e}")
            self.take_screenshot("Product Master Click Error")
            raise NavigationError(f"Failed to click 'Product Master': {e}")

        # Click Add Product button
        try:
            with allure.step("Clicking on 'Add Product' button"):
                add_product_btn = self.wait.until(ec.element_to_be_clickable(self.ADD_PRODUCT_BUTTON))
                self.safe_click(add_product_btn, "Add Product button")
                time.sleep(10)
        except Exception as e:
            logger.error(f"Error clicking 'Add Product' button: {e}")
            self.take_screenshot("Add Product Button Error")
            raise NavigationError(f"Failed to click 'Add Product': {e}")

        # Click Add Product label
        try:
            with allure.step("Clicking 'Add Product' label"):
                add_product = self.wait.until(ec.element_to_be_clickable(self.ADD_PRODUCT_LABEL))
                add_product.click()
                time.sleep(8)
        except Exception as e:
            logger.error(f"Error clicking 'Add Product' label: {e}")
            self.take_screenshot("Add Product Label Error")
            raise NavigationError(f"Failed to click 'Add Product' label: {e}")

        # Set page zoom
        self.set_page_zoom()
        time.sleep(3)

        # Handle Item Group selection
        try:
            with allure.step("Clicking on Item Group input field"):
                item_group_input = self.wait.until(ec.element_to_be_clickable(self.ITEM_GROUP_INPUT))
                item_group_input.click()
                time.sleep(5)
                item_group_input.send_keys(Keys.ENTER)
                time.sleep(5)
        except Exception as e:
            logger.error(f"Error clicking Item Group input field: {e}")
            self.take_screenshot("Item Group Input Error")
            raise FormFieldNotFoundError(f"Failed to click Item Group input field: {e}")

        # Handle Main Group selection
        try:
            with allure.step("Clicking on main group input field"):
                main_group_input = self.wait.until(ec.element_to_be_clickable(self.MAIN_GROUP_INPUT))
                main_group_input.click()
                main_group_input.send_keys(Keys.ENTER)
                main_group_input.send_keys(Keys.ENTER)
                main_group_input.send_keys(Keys.ENTER)
                time.sleep(8)

                ok_button = self.wait.until(ec.element_to_be_clickable(self.OK_BUTTON))
                ok_button.click()
        except Exception as e:
            logger.error(f"Error clicking main group input field: {e}")
            self.take_screenshot("Main Group Input Error")
            raise FormFieldNotFoundError(f"Failed to click main group input field: {e}")

        # Enter item name
        try:
            with allure.step("Entering product item name"):
                item_name_input = self.wait.until(ec.element_to_be_clickable(self.ITEM_NAME_INPUT))
                item_name_input.clear()
                item_name_input.send_keys(product_item)
                item_name_input.send_keys(Keys.ENTER)
        except Exception as e:
            logger.error(f"Error entering product item name: {e}")
            self.take_screenshot("Item Name Input Error")
            raise FormFieldNotFoundError(f"Failed to enter product item name: {e}")

        # Fill form fields using TAB navigation
        self._fill_basic_product_info(HS_code, unit, item_type, description, category, short_name)

        # Enter purchase price
        try:
            with allure.step("Entering purchase price"):
                price_input = self.wait.until(ec.element_to_be_clickable(self.PURCHASE_PRICE_INPUT))
                price_input.clear()
                price_input.send_keys(purchase_price)
                time.sleep(10)
        except Exception as e:
            logger.error(f"Error entering purchase price: {e}")
            self.take_screenshot("Purchase Price Input Error")
            raise FormFieldNotFoundError(f"Failed to enter purchase price: {e}")

        # Enter sales price
        try:
            with allure.step("Entering sales price"):
                number_input = self.wait.until(ec.element_to_be_clickable(self.SALES_PRICE_INPUT))
                number_input.clear()
                number_input.send_keys(sales_price)
                time.sleep(10)
        except Exception as e:
            logger.error(f"Error entering sales price: {e}")
            self.take_screenshot("Sales Price Input Error")
            raise FormFieldNotFoundError(f"Failed to enter sales price: {e}")

        # Handle Alternate Unit
        self._handle_alternate_unit(alt_unit, conversion_factor)

        # Handle Barcode Mapping
        self._handle_barcode_mapping(barcode_map, barcode_unit)

        # Save product
        self._save_product()

    def _fill_basic_product_info(self, HS_code, unit, item_type, description, category, short_name):
        """Fill basic product information using TAB navigation."""
        try:
            # Press Tab and enter HSC code
            self.driver.switch_to.active_element.send_keys(Keys.TAB)
            time.sleep(5)
            self.driver.switch_to.active_element.send_keys(HS_code, Keys.TAB)

            # Click vatable checkbox
            checkbox = self.wait.until(ec.element_to_be_clickable(self.VATABLE_CHECKBOX))
            checkbox.click()
            time.sleep(5)
            self.driver.switch_to.active_element.send_keys(Keys.TAB)

            # Fill remaining fields
            self.driver.switch_to.active_element.send_keys(unit, Keys.TAB)
            time.sleep(5)
            self.driver.switch_to.active_element.send_keys(item_type, Keys.TAB)
            time.sleep(5)
            self.driver.switch_to.active_element.send_keys(Keys.TAB)
            self.driver.switch_to.active_element.send_keys(description, Keys.TAB)
            time.sleep(5)
            self.driver.switch_to.active_element.send_keys(category, Keys.TAB)
            time.sleep(5)
            self.driver.switch_to.active_element.send_keys(short_name, Keys.TAB)
            time.sleep(5)

        except Exception as e:
            logger.error(f"Error filling basic product info: {e}")
            self.take_screenshot("Basic Info Error")
            raise FormFieldNotFoundError(f"Failed to fill basic product info: {e}")

    def _handle_alternate_unit(self, alt_unit, conversion_factor):
        """Handle alternate unit configuration."""
        try:
            with allure.step("Navigating to Alternate Unit tab"):
                alternate_unit_tab = self.wait.until(ec.element_to_be_clickable(self.ALTERNATE_UNIT_TAB))
                alternate_unit_tab.click()
                time.sleep(8)

            # Select unit
            select_element = self.wait.until(ec.element_to_be_clickable(self.UNIT_SELECT))
            select_element.click()
            self.driver.switch_to.active_element.send_keys(alt_unit, Keys.TAB)
            print("Unit selected.")

            # Enter conversion factor
            input_field = self.wait.until(ec.element_to_be_clickable(self.CONVERSION_FACTOR_INPUT))
            input_field.clear()
            input_field.send_keys(conversion_factor)
            time.sleep(5)

        except Exception as e:
            logger.error(f"Error handling alternate unit: {e}")
            self.take_screenshot("Alternate Unit Error")
            raise NavigationError(f"Failed to handle alternate unit: {e}")

    def _handle_barcode_mapping(self, barcode_map, barcode_unit):
        """Handle barcode mapping configuration."""
        try:
            with allure.step("Clicking on 'Add Barcode' button"):
                barcode_mapping = self.wait.until(ec.element_to_be_clickable(self.BARCODE_MAPPING_TAB))
                barcode_mapping.click()
                time.sleep(8)

            # Enter barcode
            barcode_input = self.wait.until(ec.presence_of_element_located(self.BARCODE_INPUT))
            barcode_input.clear()
            barcode_input.send_keys(barcode_map)
            barcode_input.click()
            time.sleep(5)
            self.driver.switch_to.active_element.send_keys(Keys.TAB)
            time.sleep(5)

            # Select barcode unit
            select_element = self.driver.find_element(*self.BARCODE_UNIT_SELECT)
            select_element.click()
            self.driver.switch_to.active_element.send_keys(barcode_unit, Keys.TAB)
            time.sleep(5)

            # Click Map button
            map_button = self.wait.until(ec.element_to_be_clickable(self.MAP_BUTTON))
            map_button.click()
            time.sleep(10)

        except Exception as e:
            logger.error(f"Error handling barcode mapping: {e}")
            self.take_screenshot("Barcode Mapping Error")
            raise FormFieldNotFoundError(f"Failed to handle barcode mapping: {e}")

    def _save_product(self):
        """Save the product and handle confirmation."""
        try:
            with allure.step("Clicking on 'Save' button"):
                save_button = self.driver.find_element(*self.SAVE_BUTTON)
                save_button.click()
                time.sleep(10)

            # Handle "Do you want to add another product?" alert
            with allure.step("Handling 'Do you wanna add another product?' alert"):
                body = self.driver.find_element(By.TAG_NAME, "body")
                body.send_keys(Keys.ENTER)
                time.sleep(10)

        except Exception as e:
            logger.error(f"Error saving product: {e}")
            self.take_screenshot("Save Product Error")
            raise PopupHandlingError(f"Failed to save product: {e}")