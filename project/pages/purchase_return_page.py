# pages/purchase_return_page.py

import time
import logging
import allure
import pyautogui
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from pages.base_page import BasePage
from exceptions.custom_exceptions import NavigationError, FormFieldNotFoundError, PurchaseNotSuccessError, \
    PopupHandlingError

logger = logging.getLogger(__name__)


class PurchaseReturnPage(BasePage):
    """Purchase Return page class with return functionality."""

    # Locators
    TRANSACTIONS_MENU = (By.LINK_TEXT, "Transactions")
    PURCHASE_TRANSACTION_MENU = (By.LINK_TEXT, "Purchase Transaction")
    DEBIT_NOTE_MENU = (By.LINK_TEXT, "Debit Note (Purchase Return)")
    INVOICE_NO_INPUT = (By.ID, "invoiceNO")
    REMARKS_INPUT = (By.ID, "remarksid")
    SAVE_BUTTON = (By.XPATH, "//button[contains(text(),'SAVE')]")
    BACK_BUTTON = (By.XPATH, "//button[contains(text(), 'BACK')]")

    @allure.step("Creating Purchase Return with remarks: {remarks}")
    def create_purchase_return(self, remarks):
        """Create a purchase return."""

        # Navigate to Purchase Return
        self._navigate_to_purchase_return()

        # Select invoice
        self._select_invoice()

        # Enter remarks
        self._enter_remarks(remarks)

        # Save return
        self._save_return()

        # Handle print cancellation
        self._cancel_print_invoice()

        # Navigate back
        self._navigate_back()

    def _navigate_to_purchase_return(self):
        """Navigate to Purchase Return page."""
        try:
            with allure.step("Clicking on 'Transactions' menu"):
                transaction_menu = self.driver.find_element(*self.TRANSACTIONS_MENU)
                transaction_menu.click()
                print("Clicked on 'Transactions'")

            with allure.step("Hovering over 'Purchase Transaction'"):
                purchase_transaction = self.wait.until(ec.presence_of_element_located(self.PURCHASE_TRANSACTION_MENU))
                ActionChains(self.driver).move_to_element(purchase_transaction).perform()
                time.sleep(8)

            with allure.step("Clicking on 'Purchase Return'"):
                debit_note = self.wait.until(ec.visibility_of_element_located(self.DEBIT_NOTE_MENU))
                debit_note.click()
                print("Clicked 'debit note'")
                time.sleep(8)
        except Exception as e:
            logger.error(f"Failed to navigate to Purchase Return: {e}")
            self.take_screenshot("Navigation Error")
            raise NavigationError(f"Failed to navigate to Purchase Return: {e}")

    def _select_invoice(self):
        """Select invoice for return."""
        try:
            with allure.step("Clicking on invoiceNO input field"):
                invoiceNO_input = self.driver.find_element(*self.INVOICE_NO_INPUT)
                self.driver.execute_script("arguments[0].removeAttribute('readonly')", invoiceNO_input)
                invoiceNO_input.click()
                invoiceNO_input.send_keys(Keys.ENTER)
                time.sleep(2)

                body = self.driver.find_element(By.TAG_NAME, "body")
                body.send_keys(Keys.ENTER)
                time.sleep(3)
        except Exception as e:
            logger.error(f"Failed to select invoice: {e}")
            self.take_screenshot("Invoice Selection Error")
            raise FormFieldNotFoundError(f"Failed to select invoice: {e}")

    def _enter_remarks(self, remarks):
        """Enter remarks for return."""
        try:
            with allure.step("Entering remarks for Purchase Return"):
                remarks_field = self.wait.until(ec.element_to_be_clickable(self.REMARKS_INPUT))
                time.sleep(5)
                remarks_field.clear()
                remarks_field.send_keys(remarks)
                time.sleep(5)
                print("✅ Remarks entered successfully.")
        except Exception as e:
            logger.error(f"Failed to enter remarks: {e}")
            self.take_screenshot("Remarks Input Error")
            raise FormFieldNotFoundError(f"Failed to enter remarks: {e}")

    def _save_return(self):
        """Save the return."""
        try:
            with allure.step("Clicking on 'Save' button"):
                save_button = self.driver.find_element(*self.SAVE_BUTTON)
                save_button.click()
                time.sleep(10)

            with allure.step("Handling alert after clicking 'Save' button"):
                self.wait.until(ec.alert_is_present())
                alert = self.driver.switch_to.alert
                alert.accept()
                print("Alert accepted successfully.")
        except Exception as e:
            logger.error(f"Failed to save return: {e}")
            self.take_screenshot("Save Return Error")
            raise PurchaseNotSuccessError(f"Failed to save return: {e}")

    def _cancel_print_invoice(self):
        """Cancel print invoice dialog."""
        try:
            with allure.step("Cancelling print invoice"):
                time.sleep(10)
                pyautogui.press('esc')
                time.sleep(5)
        except Exception as e:
            logger.error(f"Failed to cancel print invoice: {e}")
            self.take_screenshot("Print Invoice Cancel Error")
            raise PopupHandlingError(f"Failed to cancel print invoice: {e}")

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