# pages/purchase_return_page.py

import time
import logging
import allure
import pyautogui
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from pages.base_page import BasePage
from exceptions.custom_exceptions import NavigationError, FormFieldNotFoundError, PurchaseNotSuccessError, \
    PopupHandlingError

logger = logging.getLogger(__name__)


class PurchaseReturnPage(BasePage):
    """Purchase Return page class with return functionality."""


    def purchase_return(self, Remarks):
        wait = WebDriverWait(self.driver, 10)
        time.sleep(10)
        # Click on "Transactions"
        try:
            transaction_menu = self.driver.find_element(By.LINK_TEXT, "Transactions")
            transaction_menu.click()
            print("Clicked on 'Transactions'")
        except Exception as e:
            print("Error clicking 'Transactions':", e)
            time.sleep(10)

        # Hover over "Purchase Transaction"
        purchase_transaction = wait.until(ec.presence_of_element_located((By.LINK_TEXT, "Purchase Transaction")))
        ActionChains(self.driver).move_to_element(purchase_transaction).perform()
        time.sleep(8)

        # Wait for "Debit Note (Purchase Return)" to be visible and click it
        debit_note = wait.until(ec.visibility_of_element_located((By.LINK_TEXT, "Debit Note (Purchase Return)")))
        debit_note.click()
        print("Clicked 'debit note'")
        time.sleep(8)

        # Click on the invoiceNO input field
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

        # For remarks
        remarks_field = WebDriverWait(self.driver, 5).until(
            ec.element_to_be_clickable((By.ID, "remarksid"))
        )
        time.sleep(5)
        remarks_field.clear()
        remarks_field.send_keys(Remarks)
        time.sleep(5)
        print("✅ Remarks entered successfully.")

        time.sleep(5)

        # Click on SAVE button
        save_button = self.driver.find_element(By.XPATH, "//button[contains(text(),'SAVE')]")
        save_button.click()
        time.sleep(10)

        # Handle alert ONLY if present
        try:
            WebDriverWait(self.driver, 5).until(ec.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.accept()
            print("Alert accepted successfully.")
        except TimeoutException:
            print("No alert appeared after clicking SAVE.")

        # For closing print preview using pyautogui
        import pyautogui
        time.sleep(10)
        pyautogui.press('esc')
        time.sleep(5)

        # Click on "BACK" button
        back_btn = wait.until(ec.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'BACK')]")))
        back_btn.click()

        print("Keeping browser open for 15 seconds for observation...")
        time.sleep(10)

        # Wait until the menu is loaded
        # wait = WebDriverWait(self.driver, 10)
        # time.sleep(10)
        # # Click on "Transactions"
        # try:
        #     transaction_menu = self.driver.find_element(By.LINK_TEXT, "Transactions")
        #     transaction_menu.click()
        #     print("Clicked on 'Transactions'")
        # except Exception as e:
        #     print("Error clicking 'Transactions':", e)
        #     time.sleep(10)
        #
        # # Hover over "Purchase Transaction"
        # purchase_transaction = self.wait.until(ec.presence_of_element_located((By.LINK_TEXT, "Purchase Transaction")))
        # ActionChains(self.driver).move_to_element(purchase_transaction).perform()
        # time.sleep(8)
        #
        # # Wait for "Debit Note (Purchase Return)" to be visible and click it
        # debit_note = wait.until(ec.visibility_of_element_located((By.LINK_TEXT, "Debit Note (Purchase Return)")))
        # debit_note.click()
        # print("Clicked 'debit note'")
        # time.sleep(8)
        #
        # # Click on the invoiceNO input field
        # invoiceNO_input = self.driver.find_element(By.ID, "invoiceNO")
        # self.driver.execute_script("arguments[0].removeAttribute('readonly')", invoiceNO_input)  # Remove readonly
        # invoiceNO_input.click()
        # invoiceNO_input.send_keys(Keys.ENTER)  # First Enter to load the dropdown
        #
        # # Wait for options to appear
        # time.sleep(2)
        #
        # # Find the body element and send Enter key
        # body = self.driver.find_element(By.TAG_NAME, "body")
        # body.send_keys(Keys.ENTER)
        #
        # body = self.driver.find_element(By.TAG_NAME, "body")
        # body.send_keys(Keys.ENTER)
        #
        # time.sleep(3)
        #
        # # For remarks
        # remarks_field = WebDriverWait(self.driver, 5).until(
        #     ec.element_to_be_clickable((By.ID, "remarksid"))
        # )
        # time.sleep(5)
        # remarks_field.clear()
        # remarks_field.send_keys(Remarks)
        # time.sleep(5)
        # print("✅ Remarks entered successfully.")
        #
        # time.sleep(5)
        #
        # # Click on SAVE button
        # save_button = self.driver.find_element(By.XPATH, "//button[contains(text(),'SAVE')]")
        # save_button.click()
        # time.sleep(10)
        #
        # # Handle alert ONLY if present
        # try:
        #     WebDriverWait(self.driver, 5).until(ec.alert_is_present())
        #     alert = self.driver.switch_to.alert
        #     alert.accept()
        #     print("Alert accepted successfully.")
        # except TimeoutException:
        #     print("No alert appeared after clicking SAVE.")
        #
        # # For closing print preview using pyautogui
        # import pyautogui
        # time.sleep(10)
        # pyautogui.press('esc')
        # time.sleep(5)
        #
        # # Click on "BACK" button
        # back_btn = self.wait.until(ec.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'BACK')]")))
        # back_btn.click()
