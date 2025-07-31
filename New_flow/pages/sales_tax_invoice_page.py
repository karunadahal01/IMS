# pages/sales_tax_invoice_page.py

import time
import logging
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from pages.base_page import BasePage
from utils.helpers import generate_random_refno, generate_random_quantity, generate_random_discount
from exceptions.custom_exceptions import NavigationError, FormFieldNotFoundError, PurchaseNotSuccessError, \
    PopupHandlingError, ListNotFoundError

logger = logging.getLogger(__name__)


class SalesTaxInvoicePage(BasePage):
    """Sales Tax Invoice page class with sales functionality."""

    # Locators
    TRANSACTIONS_MENU = (By.LINK_TEXT, "Transactions" , (By.XPATH, "//a[@title='Transactions']//span[contains(text(), 'Transactions')]"))
    SALES_TRANSACTION_MENU = (By.LINK_TEXT, "Sales Transaction")
    SALES_TAX_INVOICE_MENU = (By.LINK_TEXT, "Sales Tax Invoice")
    REFNO_INPUT = (By.ID, "refnoInput")
    CUSTOMER_INPUT = (By.ID, "customerselectid")
    REMARKS_INPUT = (By.ID, "remarksid")
    BARCODE_INPUT = (By.ID, "barcodeField")
    FLAT_DISCOUNT_INPUT = (By.ID, "flatDis1")
    AFTER_BUTTON = (By.XPATH, "//button[text()='AFTER']")
    SAVE_BUTTON = (By.XPATH, "//button[contains(text(), 'SAVE') and contains(@class, 'btn-info')]")
    BALANCE_AMOUNT_BUTTON = (By.XPATH, "//button[contains(text(), 'Balance Amount') and contains(@class, 'btn-info')]")
    ADD_BUTTON = (By.XPATH, "//button[contains(text(), 'Add') and contains(@class, 'btn-info')]")
    VIEW_BUTTON = (By.XPATH, "//button[contains(text(), 'VIEW')]")
    RESET_BUTTON = (By.XPATH, "//button[contains(text(), 'RESET')]")
    BACK_BUTTON = (By.XPATH, "//button[contains(text(), 'BACK')]")

    @allure.step("Creating Sales Tax Invoice with barcode: {barcode_sales}")
    def create_sales_tax_invoice(self, barcode_sales):
        """Create a new sales tax invoice."""

        # Navigate to Sales Tax Invoice
        self._navigate_to_sales_tax_invoice()

        # Generate and enter reference number
        self._enter_reference_number()

        # Select customer
        self._select_customer()

        # Enter remarks
        self._enter_remarks("This is an automated remark for STI.")

        # Add barcode and quantity
        self._add_barcode_and_quantity(barcode_sales)

        # Show details and add flat discount
        self._show_details_and_add_discount()

        # Save invoice and handle payment
        self._save_and_handle_payment()

        # View and reset invoice
        self._view_and_reset_invoice()

        # Navigate back
        self._navigate_back()

    def _navigate_to_sales_tax_invoice(self):
        """Navigate to Sales Tax Invoice page."""
        try:
            with allure.step("Clicking on 'Transactions' menu"):
                transaction_menu = self.driver.find_element(*self.TRANSACTIONS_MENU)
                transaction_menu.click()
                print("Clicked on 'Transactions'")
                time.sleep(10)

            with allure.step("Hovering over 'Sales Transaction'"):
                sales_transaction = self.wait.until(ec.presence_of_element_located(self.SALES_TRANSACTION_MENU))
                ActionChains(self.driver).move_to_element(sales_transaction).perform()
                time.sleep(5)

            with allure.step("Clicking on 'Sales Tax Invoice'"):
                sales_tax_invoice_link = self.wait.until(ec.visibility_of_element_located(self.SALES_TAX_INVOICE_MENU))
                sales_tax_invoice_link.click()
                print("Clicked 'Sales Tax Invoice'")
                time.sleep(5)
        except Exception as e:
            logger.error(f"Failed to navigate to Sales Tax Invoice: {e}")
            self.take_screenshot("Navigation Error")
            raise NavigationError(f"Failed to navigate to Sales Tax Invoice: {e}")

    def _enter_reference_number(self):
        """Generate and enter reference number."""
        try:
            with allure.step("Generating random reference number"):
                random_refno = generate_random_refno()
                print(f"Generated Refno: {random_refno}")

                refno_input = self.driver.find_element(*self.REFNO_INPUT)
                refno_input.clear()
                refno_input.send_keys(random_refno)
                time.sleep(3)
        except Exception as e:
            logger.error(f"Error generating random reference number: {e}")
            self.take_screenshot("Reference Number Generation Error")
            raise FormFieldNotFoundError(f"Failed to generate random reference number: {e}")

    def _select_customer(self):
        """Select customer from dropdown."""
        try:
            with allure.step("Entering customer in Customer input field"):
                customer_input = self.wait.until(ec.element_to_be_clickable(self.CUSTOMER_INPUT))
                customer_input.click()
                customer_input.send_keys(Keys.ENTER)
                time.sleep(5)

                # Press ENTER on body to confirm selection
                body = self.driver.find_element(By.TAG_NAME, "body")
                body.send_keys(Keys.ENTER)
                time.sleep(10)
        except Exception as e:
            logger.error(f"Error entering customer in Customer input field: {e}")
            self.take_screenshot("Customer Input Error")
            raise FormFieldNotFoundError(f"Failed to enter customer in Customer input field: {e}")

    def _enter_remarks(self, remarks_text):
        """Enter remarks."""
        try:
            with allure.step("Entering remarks for Sales Tax Invoice"):
                remarks_field = self.wait.until(ec.element_to_be_clickable(self.REMARKS_INPUT))
                remarks_field.clear()
                remarks_field.send_keys(remarks_text)
                time.sleep(5)
                print("✅ Remarks entered successfully.")
        except Exception as e:
            logger.error(f"Failed to enter remarks: {e}")
            self.take_screenshot("Remarks Input Error")
            raise FormFieldNotFoundError(f"Failed to enter remarks: {e}")

    def _add_barcode_and_quantity(self, barcode_sales):
        """Add barcode and generate quantity."""
        try:
            with allure.step("Entering barcode for Sales Tax Invoice"):
                barcode_input = self.driver.find_element(*self.BARCODE_INPUT)
                barcode_input.clear()
                barcode_input.send_keys(barcode_sales)
                barcode_input.send_keys(Keys.ENTER)

            with allure.step("Generating random quantity for Sales Tax Invoice"):
                quantity = generate_random_quantity(10, 80)
                print(f"Generated quantity: {quantity}")

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
                        print("✅ Quantity entered and Enter key pressed.")
                        time.sleep(2)
                        break
                    except Exception as e:
                        print(f"⚠ Failed with XPath: {xpath} -> {e}")
        except Exception as e:
            logger.error(f"Failed to add barcode and quantity: {e}")
            self.take_screenshot("Barcode Quantity Error")
            raise FormFieldNotFoundError(f"Failed to add barcode and quantity: {e}")

    def _show_details_and_add_discount(self):
        """Show details and add flat discount."""
        try:
            with allure.step("Clicking on 'Show Details'"):
                body = self.driver.find_element(By.TAG_NAME, 'body')
                body.send_keys(Keys.F1)
                time.sleep(5)

            with allure.step("Adding Flat Discount"):
                flat_discount = generate_random_discount()
                print(f"Generated Flat Discount: {flat_discount}%")

                input_field = self.driver.find_element(*self.FLAT_DISCOUNT_INPUT)
                input_field.clear()
                input_field.send_keys(str(flat_discount) + Keys.ENTER)
                time.sleep(3)

                after_button = self.wait.until(ec.element_to_be_clickable(self.AFTER_BUTTON))
                after_button.click()
        except Exception as e:
            logger.error(f"Failed to show details and add discount: {e}")
            self.take_screenshot("Show Details Discount Error")
            raise FormFieldNotFoundError(f"Failed to show details and add discount: {e}")

    def _save_and_handle_payment(self):
        """Save invoice and handle payment."""
        try:
            with allure.step("Clicking on 'Save' button"):
                time.sleep(5)
                save_button = self.wait.until(ec.element_to_be_clickable(self.SAVE_BUTTON))
                save_button.click()
                time.sleep(5)

            with allure.step("Clicking on 'Balance Amount' button"):
                balance_amount_button = self.wait.until(ec.element_to_be_clickable(self.BALANCE_AMOUNT_BUTTON))
                balance_amount_button.click()
                time.sleep(5)

            # Add button
            add_button = self.wait.until(ec.element_to_be_clickable(self.ADD_BUTTON))
            add_button.click()
            time.sleep(5)

            with allure.step("Pressing 'End' key to save payment"):
                body = self.driver.find_element(By.TAG_NAME, 'body')
                body.send_keys(Keys.END)
                time.sleep(10)
        except Exception as e:
            logger.error(f"Failed to save and handle payment: {e}")
            self.take_screenshot("Save Payment Error")
            raise PurchaseNotSuccessError(f"Failed to save and handle payment: {e}")

    def _view_and_reset_invoice(self):
        """View invoice and reset form."""
        try:
            with allure.step("Viewing invoice"):
                view_button = self.wait.until(ec.element_to_be_clickable(self.VIEW_BUTTON))
                view_button.click()
                time.sleep(2)

                with allure.step("Pressing Enter to select invoice"):
                    actions = ActionChains(self.driver)
                    actions.send_keys(Keys.ENTER).perform()
                    time.sleep(5)

            with allure.step("Resetting the form"):
                reset_btn = self.wait.until(ec.element_to_be_clickable(self.RESET_BUTTON))
                reset_btn.click()
                time.sleep(5)

            with allure.step("Handling reset confirmation alert"):
                self.wait.until(ec.alert_is_present())
                alert = self.driver.switch_to.alert
                alert.accept()
                time.sleep(5)
        except Exception as e:
            logger.error(f"Failed to view and reset invoice: {e}")
            self.take_screenshot("View Reset Error")
            raise ListNotFoundError(f"Failed to view and reset invoice: {e}")

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