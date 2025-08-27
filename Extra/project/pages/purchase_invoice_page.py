
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


