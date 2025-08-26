# import allure
# import logging
# from selenium import webdriver
# from selenium.common.exceptions import WebDriverException
# from Exception.exception import WebDriverInitializationError
# from Setting import logger
#
#
#
# def setup_method(self):
#     try:
#         self.driver = webdriver.Chrome()
#         self.driver.implicitly_wait(10)
#         logger.info("WebDriver initialized successfully")
#     except WebDriverException as e:
#         logger.error(f"Failed to initialize WebDriver: {e}")
#         raise WebDriverInitializationError(f"WebDriver initialization failed: {e}")
#
#
# def teardown_method(self):
#     if hasattr(self, 'driver') and self.driver:
#         try:
#             logger.info("Cleaning up - closing driver")
#             self.driver.quit()
#             logger.info("Driver closed successfully")
#         except Exception as e:
#             logger.error(f"Error during cleanup: {e}")
#             raise WebDriverInitializationError(f"Error during driver cleanup: {e}")
#
#
# def safe_click(self, element, description="element"):
#     try:
#         element.click()
#         logger.info(f"Clicked {description} using normal click")
#     except Exception as e:
#         logger.warning(f"Normal click failed for {description}, trying JS click: {e}")
#         allure.attach(self.driver.get_screenshot_as_png(),
#                       name=f"{description} Click Error",
#                       attachment_type=allure.attachment_type.PNG)
#         self.driver.execute_script("arguments[0].click();", element)
#         logger.info(f"Clicked {description} using JavaScript click")
#
import allure
import logging
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from Exception.exception import WebDriverInitializationError

# Logging setup
logger = logging.getLogger(__name__)

def setup_method():
    """Initialize and return WebDriver instance."""
    try:
        driver = webdriver.Chrome()
        driver.implicitly_wait(10)
        logger.info("WebDriver initialized successfully")
        return driver
    except WebDriverException as e:
        logger.error(f"Failed to initialize WebDriver: {e}")
        raise WebDriverInitializationError(f"WebDriver initialization failed: {e}")


def teardown_method(driver):
    """Quit WebDriver instance."""
    if driver:
        try:
            logger.info("Cleaning up - closing driver")
            driver.quit()
            logger.info("Driver closed successfully")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
            raise WebDriverInitializationError(f"Error during driver cleanup: {e}")


def safe_click(driver, element, description="element"):
    """Click an element safely (fallback to JS click if normal click fails)."""
    try:
        element.click()
        logger.info(f"Clicked {description} using normal click")
    except Exception as e:
        logger.warning(f"Normal click failed for {description}, trying JS click: {e}")
        allure.attach(driver.get_screenshot_as_png(),
                      name=f"{description} Click Error",
                      attachment_type=allure.attachment_type.PNG)
        driver.execute_script("arguments[0].click();", element)
        logger.info(f"Clicked {description} using JavaScript click")
