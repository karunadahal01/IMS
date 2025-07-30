# utils/driver_utils.py

import logging
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from config.settings import IMPLICIT_WAIT
from exceptions.custom_exceptions import WebDriverInitializationError

logger = logging.getLogger(__name__)


class DriverManager:
    """Manages WebDriver initialization and cleanup."""

    def __init__(self):
        self.driver = None

    def initialize_driver(self):
        """Initialize Chrome WebDriver with default settings."""
        try:
            self.driver = webdriver.Chrome()
            self.driver.implicitly_wait(IMPLICIT_WAIT)
            logger.info("WebDriver initialized successfully")
            return self.driver
        except WebDriverException as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise WebDriverInitializationError(f"WebDriver initialization failed: {e}")

    def cleanup_driver(self):
        """Close and quit the WebDriver."""
        if self.driver:
            try:
                logger.info("Cleaning up - closing driver")
                self.driver.quit()
                logger.info("Driver closed successfully")
            except Exception as e:
                logger.error(f"Error during cleanup: {e}")
                raise WebDriverInitializationError(f"Error during driver cleanup: {e}")

    def get_driver(self):
        """Get the current driver instance."""
        return self.driver