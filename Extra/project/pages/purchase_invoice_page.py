# # pages/purchase_invoice_page.py
#
# import time
# import logging
# import allure
# import pyautogui
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support import expected_conditions as ec
# from selenium.common.exceptions import WebDriverException
# from pages.base_page import BasePage
# from utils.helpers import generate_random_invoice_number, generate_random_quantity, generate_random_discount
# from exceptions.custom_exceptions import NavigationError, FormFieldNotFoundError, PurchaseNotSuccessError, \
#     PopupHandlingError, ListNotFoundError
#
# logger = logging.getLogger(__name__)
#
#
# class PurchaseInvoicePage(BasePage):
#     """Purchase Invoice page class with purchase functionality."""
#
#     # Locators
#     TRANSACTIONS_MENU = (By.LINK_TEXT, "Transactions")
#     INVOICE_NO_INPUT = (By.ID, "invoiceNO")
#     REMARKS_INPUT = (By.ID, "remarksid")
#     BARCODE_INPUT = (By.ID, "barcodeField")
#     QUANTITY_XPATH = "//table//tr//td[position()=9]//input"
#     DISCOUNT_RATE_0 = (By.ID, "INDDISCOUNTRATE0")
#     DISCOUNT_RATE_1 = (By.ID, "INDDISCOUNTRATE1")
#     SAVE_BUTTON = (By.XPATH, "//button[contains(text(), 'SAVE') and contains(@class, 'btn-info')]")
#     VIEW_BUTTON = (By.XPATH, "//button[contains(text(), 'VIEW')]")
#     RESET_BUTTON = (By.XPATH, "//button[contains(text(), 'RESET')]")
#     BACK_BUTTON = (By.XPATH, "//button[contains(text(), 'BACK')]")
#
#     @allure.step("Creating Purchase Invoice with barcode: {barcode_purchase}")
#     def create_purchase_invoice(self, barcode_purchase):
#         """Create a new purchase invoice."""
#         time.sleep(5)
#
#         # Navigate to Transactions
#         self._navigate_to_purchase_invoice()
#
#         # Enter invoice number
#         self._enter_invoice_number()
#
#         # Enter account name
#         self._enter_account_name()
#
#         # Enter remarks
#         self._enter_remarks("This is an automated remark for PI.")
#
#         # Add barcode and quantity
#         self._add_barcode_and_quantity(barcode_purchase)
#
#         # Add discounts
#         self._add_discounts()
#
#         # Save invoice
#         self._save_invoice()
#
#         # Handle print cancellation
#         self._cancel_print_invoice()
#
#         # View and reset invoice
#         self._view_and_reset_invoice()
#
#         # Navigate back
#         self._navigate_back()
#
#     def _navigate_to_purchase_invoice(self):
#         """Navigate to Purchase Invoice page."""
#         try:
#             # Find and click Transactions
#             nav_elements = self.driver.find_elements(By.XPATH, "//a | //div[@class*='nav'] | //span[@class*='nav']")
#             print(f"Found {len(nav_elements)} potential navigation elements")
#
#             transactions_selectors = [
#                 "//a[contains(text(), 'Transactions')]",
#                 "//div[contains(text(), 'Transactions')]",
#                 "//span[contains(text(), 'Transactions')]",
#                 "//*[contains(@class, 'nav') and contains(text(), 'Transactions')]",
#                 "//*[text()='Transactions']",
#                 "//a[contains(@href, 'transaction')]",
#                 "//*[@class*='menu' and contains(text(), 'Transactions')]"
#             ]
#
#             for i, selector in enumerate(transactions_selectors, 1):
#                 try:
#                     print(f"  Trying selector {i}: {selector}")
#                     transactions_element = self.wait.until(ec.element_to_be_clickable((By.XPATH, selector)))
#                     actions = ActionChains(self.driver)
#                     actions.move_to_element(transactions_element).click().perform()
#                     print(f"✓ Successfully clicked on 'Transactions' using selector {i}")
#                     time.sleep(2)
#                     break
#                 except Exception as e:
#                     print(f"✗ Failed to click on 'Transactions' using selector {i}: {e}")
#                     continue
#             else:
#                 raise NavigationError("Failed to click on 'Transactions'")
#
#             # Hover over Purchase Transaction
#             self._hover_purchase_transaction()
#
#             # Click Purchase Invoice
#             self._click_purchase_invoice()
#
#         except Exception as e:
#             logger.error(f"Failed to navigate to Purchase Invoice: {e}")
#             self.take_screenshot("Navigation Error")
#             raise NavigationError(f"Failed to navigate to Purchase Invoice: {e}")
#
#     def _hover_purchase_transaction(self):
#         """Hover over Purchase Transaction menu."""
#         try:
#             all_elements = self.driver.find_elements(By.TAG_NAME, "span")
#             for element in all_elements:
#                 try:
#                     element_text = element.text.strip()
#                     if 'Purchase Transaction' in element_text and element.is_displayed():
#                         actions = ActionChains(self.driver)
#                         actions.move_to_element(element).perform()
#                         print(f"✓ Hovered over 'Purchase Transaction' using fallback method")
#                         time.sleep(2)
#                         return
#                 except WebDriverException:
#                     continue
#             raise NavigationError("Could not find or hover over 'Purchase Transaction' menu")
#         except Exception as e:
#             logger.error(f"Failed to hover over 'Purchase Transaction': {e}")
#             self.take_screenshot("Purchase Transaction Hover Error")
#             raise NavigationError(f"Failed to hover over 'Purchase Transaction': {e}")
#
#     def _click_purchase_invoice(self):
#         """Click on Purchase Invoice menu item."""
#         try:
#             with allure.step("Clicking on 'Purchase Invoice'"):
#                 purchase_invoice_selectors = [
#                     "//*[@class='dropdown-item' and contains(text(), 'Purchase Invoice')]",
#                     "//*[contains(@class, 'menu-item') and contains(text(), 'Purchase Invoice')]"
#                 ]
#
#                 for i, selector in enumerate(purchase_invoice_selectors, 1):
#                     try:
#                         print(f"  Trying Purchase Invoice selector {i}: {selector}")
#                         purchase_invoice_element = self.wait.until(ec.element_to_be_clickable((By.XPATH, selector)))
#                         actions = ActionChains(self.driver)
#                         actions.move_to_element(purchase_invoice_element).click().perform()
#                         print(f"✓ Successfully clicked on 'Purchase Invoice' using selector {i}")
#                         time.sleep(3)
#                         return
#                     except Exception as e:
#                         print(f"  ✗ Purchase Invoice selector {i} failed: {str(e)[:100]}...")
#                         continue
#
#                 # Fallback method
#                 invoice_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Purchase Invoice')]")
#                 print(f"Found {len(invoice_elements)} elements containing 'Purchase Invoice'")
#                 for element in invoice_elements:
#                     try:
#                         if element.is_displayed() and element.is_enabled():
#                             actions = ActionChains(self.driver)
#                             actions.move_to_element(element).click().perform()
#                             print(f"✓ Clicked on 'Purchase Invoice' using fallback method")
#                             time.sleep(3)
#                             return
#                     except WebDriverException:
#                         continue
#
#                 raise NavigationError("Failed to click on 'Purchase Invoice'")
#         except Exception as e:
#             logger.error(f"Failed to click on 'Purchase Invoice': {e}")
#             self.take_screenshot("Purchase Invoice Click Error")
#             raise NavigationError(f"Failed to click on 'Purchase Invoice': {e}")
#
#     def _enter_invoice_number(self):
#         """Enter random invoice number."""
#         try:
#             with allure.step("Entering Purchase Invoice number"):
#                 random_invoice = generate_random_invoice_number()
#                 print(f"Generated Invoice Number: {random_invoice}")
#
#                 invoice_field = self.wait.until(ec.element_to_be_clickable(self.INVOICE_NO_INPUT))
#                 invoice_field.clear()
#                 invoice_field.send_keys(random_invoice)
#                 print(f"✓ Successfully entered Invoice Number: {random_invoice}")
#         except Exception as e:
#             logger.error(f"Failed to enter Invoice Number: {e}")
#             self.take_screenshot("Invoice Number Input Error")
#             raise FormFieldNotFoundError(f"Failed to enter Invoice Number: {e}")
#
#     def _enter_account_name(self):
#         """Enter account name."""
#         try:
#             with allure.step("Entering Account Name"):
#                 account_field_selectors = [
#                     "//input[preceding-sibling::label[contains(text(), 'Account')] or @placeholder*='Account' or contains(@formcontrolname, 'account')]",
#                     "//input[contains(@placeholder, 'Press Enter to select Account')]",
#                     "//*[contains(text(), 'Press Enter to select Account')]",
#                     "//input[contains(@class, 'form-control') and contains(@placeholder, 'Account')]"
#                 ]
#
#                 account_field = None
#                 for selector in account_field_selectors:
#                     try:
#                         account_field = self.wait.until(ec.element_to_be_clickable((By.XPATH, selector)))
#                         print(f"✓ Found Account field using selector: {selector}")
#                         break
#                     except Exception:
#                         continue
#
#                 if account_field:
#                     account_field.click()
#                     time.sleep(1)
#                     account_field.send_keys(Keys.ENTER)
#                     print("✓ Successfully pressed Enter on Account field to open dropdown")
#                     time.sleep(3)
#                     account_field.send_keys(Keys.ENTER)
#                     print("✓ Successfully selected first account")
#                     time.sleep(2)
#                 else:
#                     raise Exception("Could not find Account field")
#         except Exception as e:
#             logger.error(f"Failed to enter Account Name: {e}")
#             self.take_screenshot("Account Name Input Error")
#             raise FormFieldNotFoundError(f"Failed to enter Account Name: {e}")
#
#     def _enter_remarks(self, remarks_text):
#         """Enter remarks."""
#         try:
#             with allure.step("Entering remarks for Purchase Invoice"):
#                 remarks_field = self.wait.until(ec.element_to_be_clickable(self.REMARKS_INPUT))
#                 remarks_field.clear()
#                 remarks_field.send_keys(remarks_text)
#                 time.sleep(5)
#                 print("✅ Remarks entered successfully.")
#         except Exception as e:
#             logger.error(f"Failed to enter remarks: {e}")
#             self.take_screenshot("Remarks Input Error")
#             raise FormFieldNotFoundError(f"Failed to enter remarks: {e}")
#
#     def _add_barcode_and_quantity(self, barcode_purchase):
#         """Add barcode and generate quantity."""
#         try:
#             with allure.step("Adding Barcode Purchase"):
#                 barcode_input = self.driver.find_element(*self.BARCODE_INPUT)
#                 barcode_input.clear()
#                 barcode_input.send_keys(barcode_purchase)
#                 barcode_input.send_keys(Keys.ENTER)
#
#             with allure.step("Generating random quantity"):
#                 quantity = generate_random_quantity(80, 200)
#                 print(f"Generated quantity: {quantity}")
#
#                 xpaths = [
#                     "//table//tr//td[position()=9]//input",
#                     "//input[contains(@name, 'quantity') or contains(@name, 'Quantity')]",
#                     "//input[contains(@id, 'quantity') or contains(@id, 'Quantity')]",
#                     "//td[contains(@class, 'quantity')]//input",
#                     "//table//tbody//tr[1]//td[9]//input",
#                 ]
#
#                 for xpath in xpaths:
#                     try:
#                         quantity_field = self.wait.until(ec.element_to_be_clickable((By.XPATH, xpath)))
#                         quantity_field.clear()
#                         quantity_field.send_keys(str(quantity) + Keys.ENTER)
#                         print("✅ Quantity entered and Enter key pressed.")
#                         time.sleep(2)
#                         break
#                     except Exception as e:
#                         print(f"⚠ Failed with XPath: {xpath} -> {e}")
#                 else:
#                     print("❌ Could not locate the quantity input field.")
#         except Exception as e:
#             logger.error(f"Failed to add barcode and quantity: {e}")
#             self.take_screenshot("Barcode Quantity Error")
#             raise FormFieldNotFoundError(f"Failed to add barcode and quantity: {e}")
#
#     def _add_discounts(self):
#         """Add random discounts."""
#         try:
#             with allure.step("Adding Discount"):
#                 discount1 = generate_random_discount()
#                 discount2 = generate_random_discount()
#
#                 print(f"Generated discount 1: {discount1}%")
#                 try:
#                     discount_field = self.wait.until(ec.element_to_be_clickable(self.DISCOUNT_RATE_0))
#                     discount_field.clear()
#                     discount_field.send_keys(str(discount1))
#                     time.sleep(2)
#                     print("✅ Discount 1 entered.")
#                 except Exception as e:
#                     print(f"❌ Discount 1 input not found: {e}")
#
#                 print(f"Generated discount 2: {discount2}%")
#                 try:
#                     discount_field = self.wait.until(ec.element_to_be_clickable(self.DISCOUNT_RATE_1))
#                     discount_field.clear()
#                     discount_field.send_keys(str(discount2))
#                     time.sleep(2)
#                     print("✅ Discount 2 entered.")
#                 except Exception as e:
#                     print(f"❌ Discount 2 input not found: {e}")
#         except Exception as e:
#             logger.error(f"Failed to add Discount: {e}")
#             self.take_screenshot("Discount Input Error")
#             raise FormFieldNotFoundError(f"Failed to add Discount: {e}")
#
#     def _save_invoice(self):
#         """Save the invoice."""
#         try:
#             with allure.step("Clicking on 'Save' button"):
#                 save_button = self.wait.until(ec.element_to_be_clickable(self.SAVE_BUTTON))
#                 save_button.click()
#
#             with allure.step("Checking for alert after clicking 'Save' button"):
#                 self.wait.until(ec.alert_is_present())
#                 alert = self.driver.switch_to.alert
#                 alert.accept()
#                 print("Alert accepted successfully.")
#         except Exception as e:
#             logger.error(f"Failed to save invoice: {e}")
#             self.take_screenshot("Save Invoice Error")
#             raise PurchaseNotSuccessError(f"Failed to save invoice: {e}")
#
#     def _cancel_print_invoice(self):
#         """Cancel print invoice dialog."""
#         try:
#             with allure.step("Cancelling print invoice"):
#                 time.sleep(10)
#                 pyautogui.press('esc')
#                 time.sleep(5)
#         except Exception as e:
#             logger.error(f"Failed to cancel print invoice: {e}")
#             self.take_screenshot("Print Invoice Cancel Error")
#             raise PopupHandlingError(f"Failed to cancel print invoice: {e}")
#
#     def _view_and_reset_invoice(self):
#         """View invoice and reset form."""
#         try:
#             with allure.step("Viewing invoice"):
#                 view_button = self.wait.until(ec.element_to_be_clickable(self.VIEW_BUTTON))
#                 view_button.click()
#                 time.sleep(2)
#
#             with allure.step("Pressing Enter to select invoice"):
#                 actions = ActionChains(self.driver)
#                 actions.send_keys(Keys.ENTER).perform()
#                 time.sleep(3)
#
#             with allure.step("Resetting the form"):
#                 reset_btn = self.wait.until(ec.element_to_be_clickable(self.RESET_BUTTON))
#                 reset_btn.click()
#
#             with allure.step("Handling reset confirmation alert"):
#                 self.wait.until(ec.alert_is_present())
#                 alert = self.driver.switch_to.alert
#                 alert.accept()
#                 time.sleep(5)
#         except Exception as e:
#             logger.error(f"Failed to view and reset invoice: {e}")
#             self.take_screenshot("View Reset Error")
#             raise ListNotFoundError(f"Failed to view and reset invoice: {e}")
#
#     def _navigate_back(self):
#         """Navigate back to dashboard."""
#         try:
#             with allure.step("Clicking on 'Back' button"):
#                 back_btn = self.wait.until(ec.element_to_be_clickable(self.BACK_BUTTON))
#                 back_btn.click()
#                 time.sleep(5)
#         except Exception as e:
#             logger.error(f"Failed to click on 'Back' button: {e}")
#             self.take_screenshot("Back Button Click Error")
#             raise NavigationError(f"Failed to click on 'Back': {e}")


import  random
import  string
import time
import logging
import allure
import pyautogui
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.wait import WebDriverWait

from pages.base_page import BasePage

from exceptions.custom_exceptions import NavigationError, FormFieldNotFoundError, PurchaseNotSuccessError, \
    PopupHandlingError, ListNotFoundError

logger = logging.getLogger(__name__)


class PurchaseInvoicePage(BasePage):
    """Purchase Invoice page class with purchase functionality."""

    ###########################################Purchase Invoice Creation#############################################################
    def purchase_invoice(self, barcode_purchase):
        global account_field
        time.sleep(10)
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
                transactions_element = WebDriverWait(self.driver, 5).until(
                    ec.element_to_be_clickable((By.XPATH, selector))
                )
                actions = ActionChains(self.driver)
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
            print("⚠️ Trying alternative approach for Purchase Invoice...")
            try:
                invoice_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Purchase Invoice')]")
                print(f"Found {len(invoice_elements)} elements containing 'Purchase Invoice'")
                for element in invoice_elements:
                    try:
                        if element.is_displayed() and element.is_enabled():
                            actions = ActionChains(self.driver)
                            actions.move_to_element(element).click().perform()
                            print(f"✓ Clicked on 'Purchase Invoice' using fallback method")
                            purchase_invoice_clicked = True
                            time.sleep(3)
                            break
                    except Exception:
                        continue
            except Exception as e:
                print(f"⚠️ Fallback method for Purchase Invoice failed: {e}")
                logger.error(f"Failed to hover over 'Purchase Transaction': {e}")
                allure.attach(self.driver.get_screenshot_as_png(),
                                  name="Transaction Hover Error",
                                  attachment_type=allure.attachment_type.PNG)
                raise NavigationError(f"Failed to hover while navigation to sales tax invoice {e}")


        print("Step 9: Manually typing in Invoice Number field...")

        ####################################################################################################
        # try:
        #     #nav_elements = self.driver.find_elements(By.XPATH, '//a | //div[@class*="nav"] | //span[@class*="nav"]')
        #     nav_elements = self.driver.find_elements(
        #         By.XPATH,
        #         '//*[self::a or self::div or self::span][contains(@class,"nav")]'
        #     )
        #
        #     print(f"Found {len(nav_elements)} potential navigation elements")
        #
        #     visible_nav_texts = []
        #     for element in nav_elements[:15]:
        #         try:
        #             text = element.text.strip()
        #             if text and len(text) > 0 and element.is_displayed():
        #                 visible_nav_texts.append(text)
        #         except WebDriverException:
        #             pass
        #
        #     print("Available navigation texts:")
        #     for text in visible_nav_texts:
        #         print(f"  - '{text}'")
        # except Exception as e:
        #     print(f"Navigation debug failed: {e}")
        #     raise NavigationError(f"Failed to Navigate: {e}")
        #
        # transactions_selectors = [
        #     "//a[contains(text(), 'Transactions')]",
        #     "//div[contains(text(), 'Transactions')]",
        #     "//span[contains(text(), 'Transactions')]",
        #     "//*[contains(@class, 'nav') and contains(text(), 'Transactions')]",
        #     "//*[text()='Transactions']",
        #     "//a[contains(@href, 'transaction')]",
        #     "//*[@class*='menu' and contains(text(), 'Transactions')]"
        # ]
        #
        # for i, selector in enumerate(transactions_selectors, 1):
        #     try:
        #         print(f"  Trying selector {i}: {selector}")
        #         transactions_element = WebDriverWait(self.driver, 5).until(
        #             ec.element_to_be_clickable((By.XPATH, selector))
        #         )
        #         actions = ActionChains(self.driver)
        #         actions.move_to_element(transactions_element).click().perform()
        #         print(f"✓ Successfully clicked on 'Transactions' using selector {i}")
        #         time.sleep(2)
        #         break  # Exit loop on success
        #
        #     except Exception as e:
        #         print(f"✗ Failed to click on 'Transactions' using selector {i}: {e}")
        #         logger.error(f"Failed to click on 'Transactions' using selector {i}: {e}")
        #         raise NavigationError(f"Failed to click on 'Transactions': {e}")
        #
        # # purchase transaction hovered
        # try:
        #     purchase_transaction_hovered = False
        #     if not purchase_transaction_hovered:
        #         print("⚠️ Trying alternative approach for Purchase Transaction hover...")
        #         try:
        #             all_elements = self.driver.find_elements(By.TAG_NAME, "span")
        #             for element in all_elements:
        #                 try:
        #                     element_text = element.text.strip()
        #                     if 'Purchase Transaction' in element_text and element.is_displayed():
        #                         actions = ActionChains(self.driver)
        #                         actions.move_to_element(element).perform()
        #                         print(f"✓ Hovered over 'Purchase Transaction' using fallback method")
        #                         purchase_transaction_hovered = True
        #                         time.sleep(2)
        #                         break
        #                 except NavigationError:
        #                     continue
        #         except Exception as e:
        #             print(f"⚠️ Fallback method for Purchase Transaction hover failed: {e}")
        #             raise NavigationError(f"Failed to hover over 'Purchase Transaction': {e}")
        #
        #     if not purchase_transaction_hovered:
        #         raise NavigationError("Could not find or hover over 'Purchase Transaction' menu")
        #
        # except Exception as e:
        #     logger.error(f"Failed to hover over 'Purchase Transaction': {e}")
        #     allure.attach(self.driver.get_screenshot_as_png(),
        #                   name="Purchase Transaction Hover Error",
        #                   attachment_type=allure.attachment_type.PNG)
        #     raise NavigationError(f"Failed to hover over 'Purchase Transaction': {e}")
        #
        # # Click on Purchase Invoice
        # try:
        #     with allure.step("Clicking on 'Purchase Invoice'"):
        #
        #         purchase_invoice_clicked = False
        #         purchase_invoice_selectors = [
        #             "//*[@class='dropdown-item' and contains(text(), 'Purchase Invoice')]",
        #             "//*[contains(@class, 'menu-item') and contains(text(), 'Purchase Invoice')]"
        #         ]
        #
        #         for i, selector in enumerate(purchase_invoice_selectors, 1):
        #             try:
        #
        #                 print(f"  Trying Purchase Invoice selector {i}: {selector}")
        #                 purchase_invoice_element = WebDriverWait(self.driver, 8).until(
        #                     ec.element_to_be_clickable((By.XPATH, selector))
        #                 )
        #                 actions = ActionChains(self.driver)
        #                 actions.move_to_element(purchase_invoice_element).click().perform()
        #                 print(f"✓ Successfully clicked on 'Purchase Invoice' using selector {i}")
        #                 purchase_invoice_clicked = True
        #                 time.sleep(3)
        #                 break
        #             except Exception as e:
        #                 print(f"  ✗ Purchase Invoice selector {i} failed: {str(e)[:100]}...")
        #                 continue
        #
        #         if not purchase_invoice_clicked:
        #             print("⚠️Trying alternative approach for Purchase Invoice...")
        #             try:
        #                 invoice_elements = self.driver.find_elements(By.XPATH,
        #                                                              "//*[contains(text(), 'Purchase Invoice')]")
        #                 print(f"Found {len(invoice_elements)} elements containing 'Purchase Invoice'")
        #                 for element in invoice_elements:
        #                     try:
        #                         if element.is_displayed() and element.is_enabled():
        #                             actions = ActionChains(self.driver)
        #                             actions.move_to_element(element).click().perform()
        #                             print(f"✓ Clicked on 'Purchase Invoice' using fallback method")
        #                             # purchase_invoice_clicked = True
        #                             time.sleep(3)
        #                             break
        #                     except NavigationError:
        #                         continue
        #             except Exception as e:
        #                 print(f"⚠️ Fallback method for Purchase Invoice failed: {e}")
        #
        #         # print("Step 9: Manually typing in Invoice Number field...")
        # except Exception as e:
        #     logger.error(f"Failed to click on 'Purchase Invoice': {e}")
        #     allure.attach(self.driver.get_screenshot_as_png(),
        #                   name="Purchase Invoice Click Error",
        #                   attachment_type=allure.attachment_type.PNG)
        #     raise NavigationError(f"Failed to click on 'Purchase Invoice': {e}")

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
                    time.sleep(10)
                    print(f"✓ Successfully entered Invoice Number: {random_invoice}")
                except Exception as e:
                    print(f"⚠️ Failed to enter Invoice Number: {e}")
        except Exception as e:
            logger.error(f"Failed to enter Invoice Number: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Invoice Number Input Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Failed to enter Invoice Number: {e}")

        # Entering Account Name
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
                    account_field = WebDriverWait(self.driver, 5).until(
                        ec.element_to_be_clickable((By.XPATH, selector))
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
                        except:
                            continue
                except Exception as e3:
                    print(f"⚠️ All methods failed to select first account: {e3}")
        ####################################################################
        # try:
        #     with allure.step("Entering Account Name"):
        #         account_field_selectors = [
        #             "//input[preceding-sibling::label[contains(text(), 'Account')] or @placeholder*='Account' or contains(@formcontrolname, 'account')]",
        #             "//input[contains(@placeholder, 'Press Enter to select Account')]",
        #             "//*[contains(text(), 'Press Enter to select Account')]",
        #             "//input[contains(@class, 'form-control') and contains(@placeholder, 'Account')]"
        #         ]
        #         account_field = None
        #         for selector in account_field_selectors:
        #             try:
        #                 account_field = WebDriverWait(self.driver, 5).until(
        #                     ec.element_to_be_clickable((By.XPATH, selector))
        #                 )
        #                 print(f"✓ Found Account field using selector: {selector}")
        #                 break
        #             except FormFieldNotFoundError:
        #                 continue
        #
        #         if account_field:
        #             account_field.click()
        #             time.sleep(1)
        #             account_field.send_keys(Keys.ENTER)
        #             print("✓ Successfully pressed Enter on Account field to open dropdown")
        #             print("⏳ Waiting for dropdown list to load completely...")
        #             time.sleep(3)
        #         else:
        #             raise Exception("Could not find Account field")
        # except Exception as e:
        #     logger.error(f"Failed to Open Account Name list: {e}")
        #     allure.attach(self.driver.get_screenshot_as_png(),
        #                   name="Account Name list Open Error",
        #                   attachment_type=allure.attachment_type.PNG)
        #     raise FormFieldNotFoundError(f"Failed to open Account Name list: {e}")
        #
        # try:
        #     with allure.step("Selecting first account from dropdown"):
        #         all_inputs = self.driver.find_elements(By.TAG_NAME, "input")
        #         for input_field in all_inputs:
        #             try:
        #                 placeholder = input_field.get_attribute("placeholder")
        #                 if placeholder and "account" in placeholder.lower():
        #                     input_field.click()
        #                     time.sleep(1)
        #                     input_field.send_keys(Keys.ENTER)
        #                     print("✓ Successfully opened Account dropdown using fallback method")
        #                     time.sleep(2)
        #                     break
        #             except FormFieldNotFoundError:
        #                 continue
        # except Exception as e2:
        #     print(f"⚠️ All methods failed to open Account dropdown: {e2}")
        #
        # print("Step 11: Selecting first account by pressing Enter again...")
        # try:
        #     with allure.step("Selecting first account by pressing Enter again"):
        #         if account_field:
        #             account_field.send_keys(Keys.ENTER)
        #             print("✓ Successfully pressed Enter again to select first account")
        #             time.sleep(2)
        #         else:
        #             focused_element = self.driver.switch_to.active_element
        #             focused_element.send_keys(Keys.ENTER)
        #             print("✓ Successfully pressed Enter on focused element to select first account")
        #             time.sleep(2)
        # except Exception as e:
        #     print(f"⚠️ Failed to select first account by pressing Enter: {e}")
        #     try:
        #         print("⚠️ Trying fallback method: Arrow Down + Enter...")
        #         if account_field:
        #             account_field.send_keys(Keys.ARROW_DOWN)
        #             time.sleep(0.5)
        #             account_field.send_keys(Keys.ENTER)
        #             print("✓ Successfully selected first account using Arrow Down + Enter")
        #         else:
        #             focused_element = self.driver.switch_to.active_element
        #             focused_element.send_keys(Keys.ARROW_DOWN)
        #             time.sleep(0.5)
        #             focused_element.send_keys(Keys.ENTER)
        #             print("✓ Successfully selected first account using Arrow Down + Enter on focused element")
        #     except Exception as e2:
        #         print(f"⚠️ All methods failed: {e2}")
        #         try:
        #             with allure.step("Last resort: Trying to click on first account directly"):
        #                 print("⚠️ Last resort: Trying to click on dropdown items...")
        #                 dropdown_selectors = [
        #                     "//div[contains(@class, 'dropdown-menu')]//a[1]",
        #                     "//ul[contains(@class, 'dropdown')]//li[1]",
        #                     "//div[contains(@class, 'dropdown')]//div[1]",
        #                     "//*[contains(@class, 'dropdown-item')][1]",
        #                     "//*[contains(@class, 'list-item')][1]"
        #                 ]
        #                 for selector in dropdown_selectors:
        #                     try:
        #                         first_account = WebDriverWait(self.driver, 3).until(
        #                             ec.element_to_be_clickable((By.XPATH, selector))
        #                         )
        #                         first_account.click()
        #                         print(f"✓ Successfully clicked on first account using selector: {selector}")
        #                         break
        #                     except FormFieldNotFoundError:
        #                         continue
        #         except Exception as e3:
        #             print(f"⚠️ All methods failed to select first account: {e3}")


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
                barcode_input.send_keys(Keys.ENTER)
        except Exception as e:
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
        except Exception as e:
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
        except Exception as e:
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
        except Exception as e:
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


