# pages/base_page.py

import logging
import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from config.settings import EXPLICIT_WAIT, PAGE_ZOOM

logger = logging.getLogger(__name__)


class BasePage:
    """Base page class with common methods for all pages."""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT)

    def safe_click(self, element, description="element"):
        """Click element with fallback to JavaScript click."""
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

    def set_page_zoom(self, zoom_level=PAGE_ZOOM):
        """Set page zoom level."""
        self.driver.execute_script(f"document.body.style.zoom='{zoom_level}'")

    def take_screenshot(self, name="screenshot"):
        """Take screenshot and attach to allure report."""
        allure.attach(self.driver.get_screenshot_as_png(),
                      name=name,
                      attachment_type=allure.attachment_type.PNG)