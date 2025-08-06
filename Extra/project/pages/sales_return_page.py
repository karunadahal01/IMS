# pages/sales_return_page.py

import time
import logging
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from pages.base_page import BasePage
from utils.helpers import generate_random_quantity
from exceptions.custom_exceptions import NavigationError, FormFieldNotFoundError, PurchaseNotSuccessError

logger = logging.getLogger(__name__)


class SalesReturnPage(BasePage):
    """Sales Return page class with return functionality."""

    # Locators
    TRANSACTIONS_MENU = (By.LINK_TEXT, "Transactions")
    SALES_TRANSACTION_MENU = (By.LINK_TEXT, "Sales Transaction")
    CREDIT_NOTE_MENU = (By.LINK_TEXT, "Credit Note (Sales Return)")
    PARTIAL_RETURN_CHECKBOX = (By.XPATH, "//input[@type='checkbox' and contains(@class, 'ng-pristine')]")
    REFBILL_INPUT = (By.ID, "refbill")
    REMARKS_INPUT = (By.ID, "remarksid")
    BARCODE_INPUT = (By.ID, "barcodeField")
    SAVE_BUTTON = (By.XPATH, "//button[contains(text(),'SAVE')]")
    BACK_BUTTON = (By.XPATH, "//button[contains(text(), 'BACK')]")

    @allure.step("Creating Sales Return (Full)")
    def create_sales_return_full(self):
        """Create a full sales return."""

        # Navigate to Sales Return
        self._navigate_to_sales_return()

        # Select reference bill
        self._select_reference_bill()

        # Enter remarks
        self._enter_remarks("sales Return by automation. ")

        # Save return
        self._save_return()

        # Navigate back
        self._navigate_back()

    @allure.step("Creating Sales Return (Partial) with barcode: {return_barcode}")
    def create_sales_return_partial(self, return_barcode):
        """Create a partial sales return."""

        # Navigate to Sales Return
        self._navigate_to_sales_return()

        # Enable partial return
        self._enable_partial_return()

        # Select reference bill
        self._select_reference_bill()

        # Enter remarks
        self._enter_remarks("Partial sales Return by automation. ")

        # Add barcode for partial return
        self._add_barcode_for_partial_return(return_barcode)

        # Save return
        self._save_return()

        # Navigate back
        self._navigate_back()

    def _navigate_to_sales_return(self):
        """Navigate to Sales Return page."""
        try:
            # Click on Transactions
            transaction_menu = self.driver.find_element(*self.TRANSACTIONS_MENU)
            transaction_menu.click()
            print("Clicked on 'Transactions'")

            # Hover over Sales Transaction
            sales_transaction = self.wait.until(ec.presence_of_element_located(self.SALES_TRANSACTION_MENU))
            ActionChains(self.driver).move_to_element(sales_transaction).perform()
            time.sleep(5)

            # Click Credit Note (Sales Return)
            with allure.step("Clicking on 'Credit Note (Sales Return)'"):
                sales_return = self.wait.until(ec.visibility_of_element_located(self.CREDIT_NOTE_MENU))
                sales_return.click()
                print("Clicked 'Credit Note (Sales Return)'")
                time.sleep(5)
        except Exception as e:
            logger.error(f"Failed to navigate to Sales Return: {e}")
            self.take_screenshot("Navigation Error")
            raise NavigationError(f"Failed to navigate to Sales Return: {e}")

    def _enable_partial_return(self):
        """Enable partial return by clicking checkbox."""
        try:
            with allure.step("Clicking on checkbox"):
                checkbox = self.wait.until(ec.element_to_be_clickable(self.PARTIAL_RETURN_CHECKBOX))
                checkbox.click()
                time.sleep(5)
        except Exception as e:
            logger.error(f"Error clicking checkbox: {e}")
            self.take_screenshot("Checkbox Click Error")
            raise NavigationError(f"Failed to click on checkbox: {e}")

    def _select_reference_bill(self):
        """Select reference bill for return."""
        try:
            with allure.step("Clicking on Ref Bill No input field"):
                refbill_input = self.driver.find_element(*self.REFBILL_INPUT)
                self.driver.execute_script("arguments[0].removeAttribute('readonly')", refbill_input)
                refbill_input.click()
                refbill_input.send_keys(Keys.ENTER)
                time.sleep(2)

                body = self.driver.find_element(By.TAG_NAME, "body")
                body.send_keys(Keys.ENTER)
                time.sleep(3)
        except Exception as e:
            logger.error(f"Failed to select reference bill: {e}")
            self.take_screenshot("Reference Bill Selection Error")
            raise FormFieldNotFoundError(f"Failed to select reference bill: {e}")

    def _enter_remarks(self, remarks_text):
        """Enter remarks for return."""
        try:
            with allure.step("Entering remarks for Sales Return"):
                remarks_field = self.wait.until(ec.element_to_be_clickable(self.REMARKS_INPUT))
                time.sleep(5)
                remarks_field.clear()
                remarks_field.send_keys(remarks_text)
                time.sleep(5)
                print("✅ Remarks entered successfully.")
        except Exception as e:
            logger.error(f"Failed to enter remarks: {e}")
            self.take_screenshot("Remarks Input Error")
            raise FormFieldNotFoundError(f"Failed to enter remarks: {e}")

    def _add_barcode_for_partial_return(self, return_barcode):
        """Add barcode for partial return with quantity."""
        try:
            with allure.step("Entering barcode for Sales Return"):
                barcode_input = self.driver.find_element(*self.BARCODE_INPUT)
                barcode_input.clear()
                barcode_input.send_keys(return_barcode)
                barcode_input.send_keys(Keys.ENTER)

                quantity = generate_random_quantity(1, 20)
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
                        quantity_field = self.wait.until(ec.element_to_be_clickable((By.XPATH, xpath)))
                        quantity_field.clear()
                        quantity_field.send_keys(str(quantity) + Keys.ENTER)
                        print(f"✅ Quantity entered for barcode {return_barcode}")
                        time.sleep(2)
                        break
                    except Exception as e:
                        print(f"⚠ Failed with XPath: {xpath} -> {e}")
                        continue
                else:
                    print(f"❌ Could not locate quantity input for barcode {return_barcode}")
                    raise FormFieldNotFoundError(f"Failed to enter quantity for barcode {return_barcode}")
        except Exception as e:
            logger.error(f"❌ Error in processing barcode '{return_barcode}': {e}")
            self.take_screenshot("Barcode Input Error")
            raise FormFieldNotFoundError(f"Failed to process barcode '{return_barcode}': {e}")

    def _save_return(self):
        """Save the return."""
        try:
            with allure.step("Clicking on 'Save' button"):
                save_button = self.driver.find_element(*self.SAVE_BUTTON)
                save_button.click()
                time.sleep(10)
        except Exception as e:
            logger.error(f"Failed to save return: {e}")
            self.take_screenshot("Save Return Error")
            raise PurchaseNotSuccessError(f"Failed to save return: {e}")

    def _navigate_back(self):
        """Navigate back to dashboard."""
        try:
            with allure.step("Clicking on 'Back' button"):
                back_btn = self.wait.until(ec.element_to_be_clickable(self.BACK_BUTTON))
                back_btn.click()
        except Exception as e:
            logger.error(f"Failed to click on 'Back' button: {e}")
            self.take_screenshot("Back Button Click Error")
            raise NavigationError(f"Failed to click on 'Back': {e}")