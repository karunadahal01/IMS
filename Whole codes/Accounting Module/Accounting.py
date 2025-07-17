import allure
import time
import logging
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
    def setup_method(self):
        try:
            self.driver = webdriver.Chrome()
            self.driver.implicitly_wait(10)
            logger.info("WebDriver initialized successfully")
        except WebDriverException as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise WebDriverInitializationError(f"WebDriver initialization failed: {e}")


    @allure.step("Teardown WebDriver")
    def __init__(self):
        self.driver = None

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
        time.sleep(10)  # Wait for the page to load after login

#################################Navigation to Accounting Module############################################################
    @allure.step("Navigate to Accounting Module")
    def navigate_to_accounting(self):
     #Accounting Module
        try:
            accounting_menu = WebDriverWait(self.driver, 10).until(
                ec.element_to_be_clickable((By.XPATH, "//span[text()='Accounting Module']"))
            )
            self.safe_click(accounting_menu, "Accounting Module")
            logger.info("Clicked on Accounting menu")
        except Exception as e:
            logger.error(f"Failed to click on Accounting menu: {e}")
            allure.attach(self.driver.get_screenshot_as_png(),
                          name="Accounting Menu Error",
                          attachment_type=allure.attachment_type.PNG)
            raise NavigationError(f"Could not navigate to Accounting module: {e}")


    def test_login(self):
         allure.step("Login to the application")
         self.login("gedehim917@decodewp.com",
               "Tebahal1!",
               "https://velvet.webredirect.himshang.com.np/#/pages/dashboard")

         self.navigate_to_accounting()

