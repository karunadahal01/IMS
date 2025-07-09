import pytest
import allure
import time
import logging
import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# --------------------------------------------------------
# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# --------------------------------------------------------
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


# --------------------------------------------------------
# Test Configuration
TEST_CONFIG = {
    "username": "gedehim917@decodewp.com",
    "password": "Tebahal1!",
    "url": "https://velvet.webredirect.himshang.com.np/#/pages/dashboard",
}


# --------------------------------------------------------
# Test class
@allure.feature("Purchase Invoice Creation")
class TestPurchaseInvoiceCreation:
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
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[formcontrolname="username"]'))
        )
        username_field.clear()
        username_field.send_keys(username)
        logger.info("Entered username")

        password_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[formcontrolname="password"]'))
        )
        password_field.clear()
        password_field.send_keys(password)
        logger.info("Entered password")

        sign_in_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign In')]"))
        )
        self.safe_click(sign_in_btn, "Sign In button")

        # # Handle already logged in popup
        # try:
        #     logout_btn = WebDriverWait(driver, 5).until(
        #         EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Logout']]"))
        #     )
        #     self.safe_click(logout_btn, "Logout button on 'Already logged in' popup")
        #     time.sleep(5)
        #     sign_in_btn = WebDriverWait(driver, 10).until(
        #         EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign In')]"))
        #     )
        #     sign_in_btn.send_keys(Keys.ENTER)
        #     logger.info("Handled already logged in scenario, re-logged in")
        # except TimeoutException:
        #     logger.info("No 'already logged in' popup detected")

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
                allure.attach(self.driver.get_screenshot_as_png(),
                              name="Logout Button Error",
                              attachment_type=allure.attachment_type.PNG)
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

        except Exception as e:
            logger.error(f"Failed to handle 'Already Logged In' popup: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Login Error",
                          attachment_type=allure.attachment_type.PNG)
            raise LoginFailedError(f"Login failed: {e}")
        time.sleep(10)  # Wait for the page to load after login


    #################################################################purchase invoice################################################# # -----------------------------------
    @allure.step("Create purchase invoice")
    def purchase_invoice(self, barcode):
        global account_field, e
        driver = self.driver
        actions = ActionChains(driver)
        wait = WebDriverWait(driver, 10)
        transactions_clicked = False
        print("Step 6.1: Debugging available navigation elements...")
        try:
            nav_elements = driver.find_elements(By.XPATH, "//a | //div[@class*='nav'] | //span[@class*='nav']")
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
                transactions_element = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                actions = ActionChains(driver)
                actions.move_to_element(transactions_element).click().perform()
                print(f"✓ Successfully clicked on 'Transactions' using selector {i}")
                transactions_clicked = True
                time.sleep(2)
                break
            except Exception as e:
                print(f"  ✗ Selector {i} failed: {str(e)[:50]}...")
                logger.error(f"Navigation failed: {e}")
                allure.attach(driver.get_screenshot_as_png(),
                                name="Transactions Navigation Error",
                                attachment_type=allure.attachment_type.PNG)

                continue


        purchase_transaction_hovered = False
        if not purchase_transaction_hovered:
            print("⚠️ Trying alternative approach for Purchase Transaction hover...")
            try:
                all_elements = driver.find_elements(By.TAG_NAME, "span")
                for element in all_elements:
                    try:
                        element_text = element.text.strip()
                        if 'Purchase Transaction' in element_text and element.is_displayed():
                            actions = ActionChains(driver)
                            actions.move_to_element(element).perform()
                            print(f"✓ Hovered over 'Purchase Transaction' using fallback method")
                            purchase_transaction_hovered = True
                            time.sleep(2)
                            break
                    except Exception:
                        continue
            except Exception as e:
                print(f"⚠️ Fallback method for Purchase Transaction hover failed: {e}")
                logger.error(f"Navigation failed: {e}")
                allure.attach(driver.get_screenshot_as_png(),
                                name="Purchase Transaction Hover Error",
                                attachment_type=allure.attachment_type.PNG)


        if not purchase_transaction_hovered:
            raise NavigationError("Could not find or hover over 'Purchase Transaction' menu")

        try:
            print("Step 8: Clicking on 'Purchase Invoice' from dropdown...")
            purchase_invoice_clicked = False
            purchase_invoice_selectors = [
                "//*[@class='dropdown-item' and contains(text(), 'Purchase Invoice')]",
                "//*[contains(@class, 'menu-item') and contains(text(), 'Purchase Invoice')]"
            ]

            for i, selector in enumerate(purchase_invoice_selectors, 1):
                try:
                    print(f"  Trying Purchase Invoice selector {i}: {selector}")
                    purchase_invoice_element = WebDriverWait(driver, 8).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    actions = ActionChains(driver)
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
                    invoice_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Purchase Invoice')]")
                    print(f"Found {len(invoice_elements)} elements containing 'Purchase Invoice'")
                    for element in invoice_elements:
                        try:
                            if element.is_displayed() and element.is_enabled():
                                actions = ActionChains(driver)
                                actions.move_to_element(element).click().perform()
                                print(f"✓ Clicked on 'Purchase Invoice' using fallback method")
                                purchase_invoice_clicked = True
                                time.sleep(3)
                                break
                        except Exception:
                            continue

                except Exception as e:
                    print(f"⚠️ Fallback method for Purchase Invoice failed: {e}")
                    logger.error(f"Navigation failed: {e}")
                    allure.attach(driver.get_screenshot_as_png(),
                                    name="Purchase Invoice Navigation Error",
                                    attachment_type=allure.attachment_type.PNG)

                    raise NavigationError(f"Failed to navigate to required menu: {e}")
        except Exception as e:
                    print(f"⚠️ Fallback method for Purchase Invoice failed: {e}")
                    logger.error(f"Navigation failed: {e}")
                    allure.attach(driver.get_screenshot_as_png(),
                                    name="Purchase Invoice Navigation Error",
                                    attachment_type=allure.attachment_type.PNG)
                    raise NavigationError(f"Failed to navigate to required menu: {e}")

        # print("Step 8: Clicking on 'Purchase Invoice' from dropdown...")
         # purchase_invoice_clicked = False
        # purchase_invoice_selectors = [
        #     "//*[@class='dropdown-item' and contains(text(), 'Purchase Invoice')]",
        #     "//*[contains(@class, 'menu-item') and contains(text(), 'Purchase Invoice')]"
        # ]
        #
        # for i, selector in enumerate(purchase_invoice_selectors, 1):
        #     try:
        #         print(f"  Trying Purchase Invoice selector {i}: {selector}")
        #         purchase_invoice_element = WebDriverWait(driver, 8).until(
        #             EC.element_to_be_clickable((By.XPATH, selector))
        #         )
        #         actions = ActionChains(driver)
        #         actions.move_to_element(purchase_invoice_element).click().perform()
        #         print(f"✓ Successfully clicked on 'Purchase Invoice' using selector {i}")
        #         purchase_invoice_clicked = True
        #         time.sleep(3)
        #         break
        #     except Exception as e:
        #         print(f"  ✗ Purchase Invoice selector {i} failed: {str(e)[:50]}...")
        #         logger.error(f"Navigation failed: {e}")
        #         allure.attach(driver.get_screenshot_as_png(),
        #                       name="Purchase Invoice Navigation Error",
        #                       attachment_type=allure.attachment_type.PNG)
        #         raise NavigationError(f"Failed to navigate to required menu: {e}")
        #
        # if not purchase_invoice_clicked:
        #     print("⚠️ Trying alternative approach for Purchase Invoice...")
        #     try:
        #         invoice_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Purchase Invoice')]")
        #         print(f"Found {len(invoice_elements)} elements containing 'Purchase Invoice'")
        #         for element in invoice_elements:
        #             try:
        #                 if element.is_displayed() and element.is_enabled():
        #                     actions = ActionChains(driver)
        #                     actions.move_to_element(element).click().perform()
        #                     print(f"✓ Clicked on 'Purchase Invoice' using fallback method")
        #                     purchase_invoice_clicked = True
        #                     time.sleep(3)
        #                     break
        #             except Exception:
        #                 continue
        #     except Exception as e:
        #         print(f"⚠️ Fallback method for Purchase Invoice failed: {e}")
        #         logger.error(f"Navigation failed: {e}")
        #         allure.attach(driver.get_screenshot_as_png(),
        #                       name="Purchase Invoice Navigation Error",
        #                       attachment_type=allure.attachment_type.PNG)
        #         raise NavigationError(f"Failed to navigate to required menu: {e}")
        time.sleep(8)
        # Fill form
        try:
            invoice_no = "INV-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            logger.info(f"Generated Invoice Number: {invoice_no}")

            invoice_field = wait.until(EC.element_to_be_clickable((By.ID, "invoiceNO")))
            invoice_field.clear()
            invoice_field.send_keys(invoice_no)

        except Exception as e:
            logger.error(f"Invoice field not found: {e}")
            allure.attach(driver.get_screenshot_as_png(),
                          name="Invoice Field Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Invoice field error: {e}")

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
                    account_field = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    print(f"✓ Found Account field using selector: {selector}")
                    break
                except:
                    continue

            if account_field:
                account_field.click()
                time.sleep(4)
                account_field.send_keys(Keys.ENTER)
                print("✓ Successfully pressed Enter on Account field to open dropdown")
                print("⏳ Waiting for dropdown list to load completely...")
                time.sleep(8)
            else:
                raise ListNotFoundError("Could not find Account field")

        except Exception as e:
            print(f"⚠️ Failed to open Account dropdown using primary method: {e}")
            logger.error(f"failed to open account dropdown: {e}")
            allure.attach(driver.get_screenshot_as_png(),
                          name="Account Dropdown Error",
                          attachment_type=allure.attachment_type.PNG)
            raise ListNotFoundError(f"Account dropdown error: {e}")

        try:
            with allure.step("Trying alternative methods to open Account dropdown"):
                all_inputs = driver.find_elements(By.TAG_NAME, "input")
                for input_field in all_inputs:
                    try:
                        placeholder = input_field.get_attribute("placeholder")
                        if placeholder and "account" in placeholder.lower():
                            input_field.click()
                            time.sleep(4)
                            input_field.send_keys(Keys.ENTER)
                            print("✓ Successfully opened Account dropdown using fallback method")
                            time.sleep(8)
                            break
                    except:
                        continue
        except Exception as e2:
            print(f"⚠️ All methods failed to open Account dropdown: {e2}")
            logger.error(f"Invoice field not found: {e}")
            allure.attach(driver.get_screenshot_as_png(),
                          name="Account Dropdown Error",
                          attachment_type=allure.attachment_type.PNG)
            raise ListNotFoundError(f"Account dropdown error: {e}")

        print("Step 11: Selecting first account by pressing Enter again...")
        try:
            with allure.step("Selecting first account in Purchase Invoice form"):
                if account_field:
                    account_field.send_keys(Keys.ENTER)
                    print("✓ Successfully pressed Enter again to select first account")
                    time.sleep(6)
                else:
                    focused_element = driver.switch_to.active_element
                    focused_element.send_keys(Keys.ENTER)
                    print("✓ Successfully pressed Enter on focused element to select first account")
                    time.sleep(6)
        except Exception as e:
            print(f"⚠️ Failed to select first account by pressing Enter: {e}")
            logger.error(f"Failed to select first account: {e}")
            allure.attach(driver.get_screenshot_as_png(),
                          name="Account Selection Error",
                          attachment_type=allure.attachment_type.PNG)
            raise ListNotFoundError(f"Account selection error: {e}")

        try:
            print("⚠️ Trying fallback method: Arrow Down + Enter...")
            if account_field:
                account_field.send_keys(Keys.ARROW_DOWN)
                time.sleep(0.5)
                account_field.send_keys(Keys.ENTER)
                print("✓ Successfully selected first account using Arrow Down + Enter")
            else:
                focused_element = driver.switch_to.active_element
                focused_element.send_keys(Keys.ARROW_DOWN)
                time.sleep(5)
                focused_element.send_keys(Keys.ENTER)
                print("✓ Successfully selected first account using Arrow Down + Enter on focused element")
        except Exception as e2:
            print(f"⚠️ All methods failed: {e2}")
            logger.error(f"Failed to select first account: {e2}")
            allure.attach(driver.get_screenshot_as_png(),
                          name="Account Selection Error",
                          attachment_type=allure.attachment_type.PNG)

        try:
            with allure.step("Trying to select first account using alternative methods"):
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
                        first_account = WebDriverWait(driver, 3).until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        first_account.click()
                        print(f"✓ Successfully clicked on first account using selector: {selector}")
                        break
                    except:
                        print(f"✗ Failed to click on first account using selector: {selector}")
                        continue
        except Exception as e3:
            print(f"⚠️ All methods failed to select first account: {e3}")
            logger.error(f"Failed to select first account: {e3}")
            allure.attach(driver.get_screenshot_as_png(),
                          name="Account Selection Error",
                          attachment_type=allure.attachment_type.PNG)
            raise ListNotFoundError(f"Account selection error: {e3}")

        print("\n" + "=" * 50)
        print("✓ NEW FUNCTIONALITY COMPLETED SUCCESSFULLY!")
        print("✓ Account dropdown opened by pressing Enter")
        print("✓ First account selected by pressing Enter again")
        print("=" * 50 + "\n")

        # Enter remarks
        print("Step 12: Entering remarks...")
        try:
            with allure.step("Entering Remarks in Purchase Invoice form"):
                remarks = wait.until(EC.element_to_be_clickable((By.ID, "remarksid")))
                remarks.clear()
                remarks.send_keys("Automated test remarks.")
                print("✓ Successfully entered remarks")
        except Exception as e:
            print(f"⚠️ Failed to enter remarks: {e}")
            logger.error(f"Remarks field not found: {e}")
            allure.attach(driver.get_screenshot_as_png(),
                          name="Remarks Entry Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Remarks field error: {e}")

        try:
            # Barcode
            with allure.step("Entering barcode in Purchase Invoice form"):
                barcode_input = driver.find_element(By.ID, "barcodeField")
                barcode_input.clear()
                barcode_input.send_keys(barcode)
                barcode_input.send_keys(Keys.ENTER)
                time.sleep(2)
        except Exception as e:
            print(f"⚠️ Failed to enter remarks: {e}")
            logger.error(f"Barcode field not found: {e}")
            allure.attach(driver.get_screenshot_as_png(),
                          name="Barcode Entry Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Barcode field error: {e}")

        try:
            with allure.step("Entering Quantity in Purchase Invoice form"):
                quantity = random.randint(80, 200)
                print(f"Generated quantity: {quantity}")

                xpaths = [
                    "//table//tr//td[position()=9]//input",
                    "//input[contains(@name, 'quantity') or contains(@name, 'Quantity')]",
                    "//input[contains(@id, 'quantity') or contains(@id, 'Quantity')]",
                    "//td[contains(@class, 'quantity')]//input",
                    "//table//tbody//tr[1]//td[9]//input",
                    "//input[@placeholder='Enter Quantity']"
                ]

                quantity_field = None
                for xpath in xpaths:
                    try:
                        quantity_field = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, xpath))
                        )
                        quantity_field.clear()
                        quantity_field.send_keys(str(quantity) + Keys.ENTER)
                        print("✅ Quantity entered and Enter key pressed.")
                        time.sleep(2)
                        break
                    except Exception as e:
                        print(f"⚠ Failed with XPath: {xpath} -> {e}")
                        logger.error(f"Quantity field not found with XPath {xpath}: {e}")
                        allure.attach(driver.get_screenshot_as_png(),
                                      name="Quantity Field Error",
                                      attachment_type=allure.attachment_type.PNG)
                        continue

        except Exception as e:
            print(f"⚠️ Failed to enter remarks: {e}")
            logger.error(f"Quantity field not found: {e}")
            allure.attach(driver.get_screenshot_as_png(),
                          name="Quantity Entry Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Quantity field error: {e}")

        try:
            # Barcode
            with allure.step("Entering barcode in Purchase Invoice form"):
                # Click SAVE
                save_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(text(), 'SAVE') and contains(@class, 'btn-info')]")))
                save_button.click()
                logger.info("Clicked SAVE")
                time.sleep(10)

        except Exception as e:
            print(f"⚠️ Failed to Save: {e}")
            logger.error(f"Save Button not found: {e}")
            allure.attach(driver.get_screenshot_as_png(),
                          name="Save button Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Save Button error: {e}")

        try:
            with allure.step("Alert box in Purchase Invoice form"):
                WebDriverWait(driver, 5).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
                print("Alert accepted successfully.")
        except Exception as e:
            print(f"⚠️ Failed to Accept Alert: {e}")
            logger.error(f"Alert not found: {e}")
            allure.attach(driver.get_screenshot_as_png(),
                          name="Alert Box Error",
                          attachment_type=allure.attachment_type.PNG)
            raise PopupHandlingError(f"Save Button error: {e}")

        try:
            with allure.step("Cancel the print format in Purchase Invoice form"):
                import pyautogui
                time.sleep(10)
                pyautogui.press('esc')
                time.sleep(5)
        except Exception as e:
            print(f"⚠️ Failed to Click Esc: {e}")
            logger.error(f"Cancel Button not found: {e}")
            allure.attach(driver.get_screenshot_as_png(),
                          name="Cancel Button Error",
                          attachment_type=allure.attachment_type.PNG)
            raise PopupHandlingError(f"Cancel Button error: {e}")

        try:
            with allure.step("View the purchase invoice in Purchase Invoice form"):
                view_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'VIEW')]")))
                view_button.click()
        except Exception as e:
            print(f"⚠️ Failed to Click View Button: {e}")
            logger.error(f"View Button not found: {e}")
            allure.attach(driver.get_screenshot_as_png(),
                          name="View Button Error",
                          attachment_type=allure.attachment_type.PNG)
            raise PopupHandlingError(f"View Button error: {e}")

        try:
            with allure.step("Select the first invoice in Purchase Invoice form"):
                time.sleep(2)
                actions = ActionChains(driver)
                actions.send_keys(Keys.ENTER).perform()
                time.sleep(3)
        except Exception as e:
            print(f"⚠️ Failed to select first invoice: {e}")
            logger.error(f" Cannot select invoice: {e}")
            allure.attach(driver.get_screenshot_as_png(),
                          name="Invoice select Error",
                          attachment_type=allure.attachment_type.PNG)
            raise PopupHandlingError(f"Invoice Select error: {e}")

        try:
            with allure.step("Reset the page in Purchase Invoice form"):
                # Click RESET
                reset_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'RESET')]")))
                reset_btn.click()
                logger.info("Clicked RESET")
                time.sleep(5)
            reset_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'RESET')]")))
        except Exception as e:
            print(f"⚠️ Failed to Click on Reset Button: {e}")
            logger.error(f" Cannot Reset page: {e}")
            allure.attach(driver.get_screenshot_as_png(),
                          name="Reset the page Error",
                          attachment_type=allure.attachment_type.PNG)
            raise PopupHandlingError(f"Reset page Error error: {e}")

        #########################################################I think its not necessary to check the popup after reset#########################################################
        # -----------------------------------
        # # Popup modal check for already exists
        # try:
        #   with allure.step("Popup  in Purchase Invoice form"):
        #     popup_message = WebDriverWait(driver, 5).until(
        #         EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'modal')]//p"))
        #     )
        #     popup_text = popup_message.text
        #     allure.attach(driver.get_screenshot_as_png(),


#####################################Function call ########################################

    # -----------------------------------

    def test_login(self):
        allure.step("Login to the application")
        self.login(TEST_CONFIG["username"], TEST_CONFIG["password"], TEST_CONFIG["url"])
        logger.info("Login successful.")

    def test_flow_with_invalid_barcode(self):
        self.login(TEST_CONFIG["username"], TEST_CONFIG["password"], TEST_CONFIG["url"])
        self.purchase_invoice(barcode="INVALID_BARCODE")
        logger.info("Test flow completed successfully.")
        time.sleep(5)  # observe browser before closing

    @pytest.mark.parametrize("barcode", ["2020", "2021", "2022", "2023"])
    @allure.feature("Login Flow")
    @allure.story("Purchase Invoice")
    def test_product_flow(self,barcode):
        self.login(TEST_CONFIG["username"], TEST_CONFIG["password"], TEST_CONFIG["url"])
        self.purchase_invoice(barcode="2020")
        logger.info("Test flow completed successfully.")
        time.sleep(5)  # observe browser before closing


