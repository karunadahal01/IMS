#import pytest
import allure
import time
import logging
import random
import string
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains




# Logging setup
logging.basicConfig(level=logging.INFO, format='%(pastime)s - %(levelness)s - %(message)s')
logger = logging.getLogger(__name__)


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

