import allure
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import string
import random
import pyautogui
from selenium.webdriver.common.action_chains import ActionChains


#--------------------------------------------------------
# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


#################################################################################################
# Custom Exceptions
class LoginFailedError(Exception):
    """Raised when login fails due to invalid credentials or unexpected errors."""
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

class ListNotFoundError(Exception):
    """Raised when saving the sales invoice fails."""
    pass

class AccountingError(Exception):
    """Raised when saving the sales invoice fails."""
    pass

#################################################################################################


# Test class
@allure.feature("Test ERP FLow Creation")
class TestERPFlowCreation:


    @allure.step("Setup WebDriver")
    def setup_method(self, method):
        try:
            self.driver = webdriver.Chrome()
            self.driver.implicitly_wait(10)
            logger.info("WebDriver initialized successfully")
        except WebDriverException as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise WebDriverInitializationError(f"WebDriver initialization failed: {e}")


    @allure.step("Teardown WebDriver")
    def teardown_method(self, method):
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
        time.sleep(20)  # Wait for the page to load after login

#################################Navigation to Accounting Module############################################################
    @allure.step("Navigate to Accounting Module")
    def navigate_to_accounting(self ,ledgeraccount1, ledgeraccount2):
     #Accounting Module
        try:
            wait = WebDriverWait(self.driver, 10)
            time.sleep(5)
            accounting_menu =self.driver.find_element(By.LINK_TEXT, "Accounting Module")
            accounting_menu.click()
            # Wait for new tab to open
            wait.until(lambda d: len(d.window_handles) > 1)

            # Switch to the new tab
            self.driver.switch_to.window(self.driver.window_handles[1])

            # Wait until URL contains WEBACCOUNTREDIRECT
            wait.until(ec.url_contains("WEBACCOUNTREDIRECT"))

            # ✅ Now you can continue actions on the new tab
            print("Now working in:", self.driver.current_url)
            #self.safe_click(accounting_menu, "Accounting Module")
            logger.info("Clicked on Accounting menu")
        except Exception as e:
            logger.error(f"Failed to click on Accounting menu: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Accounting Menu Error",
                          attachment_type=allure.attachment_type.PNG)
            raise NavigationError(f"Could not navigate to Accounting module: {e}")

        #Navigate to Transactions
        try:
            time.sleep(5)
            transactions_menu = WebDriverWait(self.driver, 10).until(
                ec.element_to_be_clickable(
                    (By.XPATH, "//a[contains(@class, 'main-menu-button') and contains(., 'Transactions')]"))
            )
            self.safe_click(transactions_menu, "Transactions menu")
            logger.info("Successfully clicked on Transactions menu")
        except Exception  as e:
            logger.error(f"Failed to click on Transactions menu: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Transactions Menu Error",
                          attachment_type=allure.attachment_type.PNG)
            raise NavigationError(f"Could not navigate to Transactions: {e}")

        #Navigate to Voucher Entries
        try:
            time.sleep(10)
            voucher_entries_menu = self.driver.find_element(By.LINK_TEXT, "Voucher Entries")
            voucher_entries_menu.click()
            logger.info("Clicked on Voucher Entries menu")
        except Exception as e:
            logger.error(f"Failed to click on Voucher Entries menu: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Voucher Entries Menu Error",
                          attachment_type=allure.attachment_type.PNG)
            raise NavigationError(f"Could not navigate to Voucher Entries: {e}")

        # CLick on Dropdown named contra Voucher
        try:
            time.sleep(5)
            # journal_voucher_dropdown = WebDriverWait(self.driver, 10).until(
            #     ec.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'dropdown-toggle') and contains(., 'Journal Voucher')]"))
            # )
            # self.safe_click(journal_voucher_dropdown, "Journal Voucher dropdown")
            sales_tax_invoice = wait.until(ec.visibility_of_element_located((By.LINK_TEXT, "Contra Voucher")))
            sales_tax_invoice.click()
            time.sleep(10)
            logger.info("Clicked on contra Voucher dropdown")
        except Exception as e:
            logger.error(f"Failed to click on contra Voucher dropdown: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="contra Voucher Dropdown Error",
                          attachment_type=allure.attachment_type.PNG)
            raise NavigationError(f"Could not navigate to contra Voucher: {e}")

         # Generate Random Refno

        # pyautogui.click()

        body = self.driver.find_element(By.TAG_NAME, "body")

        # Perform click
        body.click()
        try:

            time.sleep(5)
            # ref_no_field = WebDriverWait(self.driver, 10).until(
            #     ec.element_to_be_clickable((By.XPATH, "//input[@formcontrolname='refNo']"))
            # )
            # ref_no_field.clear()
            # ref_no_field.send_keys("RefNo-" + str(int(time.time())))

            def generate_random_refno(length=8):
                digits = string.digits
                return ''.join(random.choice(digits) for i in range(length))

            # Generate the random refno
            random_refno = generate_random_refno()
            print(f"Generated Refno: {random_refno}")

            # Find the input field by ID and input the random refno
            refno_input = self.driver.find_element(By.ID, "refno")
            refno_input.clear()
            refno_input.send_keys(random_refno)

            time.sleep(3)
            logger.info("Entered random RefNo")
        except Exception as e:
            logger.error(f"Failed to enter RefNo: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="RefNo Field Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Could not find or interact with RefNo field: {e}")
#########################################################################################
        # Entering Account first ledger
        try:
            time.sleep(5)
            wait = WebDriverWait(self.driver, 10)
            ledger1 = wait.until(ec.presence_of_element_located((By.ID, "ACCODEInput_0")))
            ledger1.send_keys(Keys.ENTER)
            time.sleep(5)
            self.driver.switch_to.active_element.send_keys(ledgeraccount1 )
           # self.driver.switch_to.active_element.send_keys(Keys.ARROW_DOWN)
            self.driver.switch_to.active_element.send_keys(Keys.ENTER)


            time.sleep(5)
            logger.info("Entered first Account Ledger")
        except Exception as e:
            logger.error(f"Failed to enter first Account Ledger: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Account Ledger Field Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Could not find or interact with Account Ledger field: {e}")

        # Entering Amount for first ledger
        try:
            wait = WebDriverWait(self.driver, 10)
            input_field = wait.until(ec.visibility_of_element_located((By.ID, "DrAmtInput_0")))

            # Clear any existing value and insert your new value
            input_field.clear()
            input_field.send_keys("100")
            self.driver.switch_to.active_element.send_keys(Keys.TAB , Keys.TAB, Keys.TAB)
            # self.driver.switch_to.active_element.send_keys(Keys.ENTER)
            wait = WebDriverWait(self.driver, 10)  # Wait up to 10 seconds
            narration_field = wait.until(ec.element_to_be_clickable((By.ID, "narration_0")))

            # Click on the element
            narration_field.click()
            narration_field.send_keys(Keys.ENTER)
            narration_field.send_keys(Keys.ENTER)
            print("Successfully clicked the 'narration_0' field.")

            # time.sleep(5)
            # self.driver.switch_to.active_element.send_keys('100')
            # self.driver.switch_to.active_element.send_keys('100', Keys.TAB)
            # time.sleep(3)
            logger.info("Entered Amount for first ledger")

        except Exception as e:
            logger.error(f"Failed to enter Amount for first ledger: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Amount Field Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Could not find or interact with Amount field: {e}")



        #Press enter in narration to add another ledger
        try:

            self.driver.switch_to.active_element.send_keys( Keys.ENTER)
            logger.info("Pressed Enter to add another ledger")

        except Exception as e:
            logger.error(f"Failed to press Enter for adding another ledger: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Enter Key Error",
                          attachment_type=allure.attachment_type.PNG)
            raise FormFieldNotFoundError(f"Could not press Enter key: {e}")
##############################################################################################
            # Entering Account second ledger
        try:
                time.sleep(5)
                wait = WebDriverWait(self.driver, 10)
                ledger2 = wait.until(ec.presence_of_element_located((By.ID, "ACCODEInput_1")))
                ledger2.send_keys(Keys.ENTER)
                time.sleep(5)
                self.driver.switch_to.active_element.send_keys(ledgeraccount2)
                self.driver.switch_to.active_element.send_keys(Keys.ARROW_DOWN)
                self.driver.switch_to.active_element.send_keys(Keys.ENTER)
                time.sleep(5)
                logger.info("Entered first Account Ledger")
        except Exception as e:
                logger.error(f"Failed to enter first Account Ledger: {e}")
                allure.attach(self.driver.get_screenshot_as_png(),
                              name="Account Ledger Field Error",
                              attachment_type=allure.attachment_type.PNG)
                raise FormFieldNotFoundError(f"Could not find or interact with Account Ledger field: {e}")

        # Entering Amount for second ledger
        try:

                self.driver.switch_to.active_element.send_keys(Keys.TAB)
                self.driver.switch_to.active_element.send_keys(Keys.ENTER)
                self.driver.switch_to.active_element.send_keys('100')
                time.sleep(3)

                time.sleep(5)
                logger.info("Entered Amount for second ledger")
        except Exception as e:
                logger.error(f"Failed to enter Amount for Second ledger: {e}")
                allure.attach(self.driver.get_screenshot_as_png(),
                              name="Amount Field Error",
                              attachment_type=allure.attachment_type.PNG)
                raise FormFieldNotFoundError(f"Could not find or interact with Amount field: {e}")

    ######################################################################################

        #saving the voucher
        try:
            #self.driver.switch_to.active_element.send_keys(Keys.SHIFT)
            time.sleep(5)
            save_button = self.driver.find_element(By.XPATH, "//button[contains(text(),'SAVE')]")
            save_button.click()

            logger.info("Clicked on Save button")
        except Exception as e:
            logger.error(f"Failed to click on Save button: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Save Button Error",
                          attachment_type=allure.attachment_type.PNG)
            raise AccountingError(f"Could not save the voucher: {e}")
        #Print alert Handle
        try:
           time.sleep(6)
           self.driver.switch_to.active_element.send_keys(Keys.ENTER)
           time.sleep(6)
           self.driver.switch_to.active_element.send_keys(Keys.ENTER)
           time.sleep(6)
           self.driver.switch_to.active_element.send_keys(Keys.ENTER)
        except Exception as e:
            logger.error(f"Failed to handle alert after saving: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Alert Handling Error",
                          attachment_type=allure.attachment_type.PNG)
            raise PopupHandlingError(f"Could not handle alert after saving: {e}")


        time.sleep(10)

    allure.step("Login to the application")
    def test_login(self):
         self.login("gedehim917@decodewp.com",
               "Tebahal1!",
               "https://velvet.webredirect.himshang.com.np/#/pages/dashboard")

         self.navigate_to_accounting(ledgeraccount1="PURCHASE A/C" , ledgeraccount2="PURCHASE A/C")

    time.sleep(10)
