# pages/login_page.py

import time
import logging
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from pages.base_page import BasePage
from exceptions.custom_exceptions import LoginFailedError

logger = logging.getLogger(__name__)


class LoginPage(BasePage):
    """Login page class with login functionality."""

    # Locators
    USERNAME_INPUT = (By.CSS_SELECTOR, 'input[formcontrolname="username"]')
    PASSWORD_INPUT = (By.CSS_SELECTOR, 'input[formcontrolname="password"]')
    SIGN_IN_BUTTON = (By.XPATH, "//button[contains(text(), 'Sign In')]")
    LOGOUT_BUTTON = (By.XPATH, "//button[.//span[text()='Logout']]")

    @allure.step("Login with username: {username}")
    def login(self, username, password, link):
        """Login to the application."""
        driver = self.driver
        driver.maximize_window()
        driver.get(link)
        logger.info(f"Navigated to: {link}")

        # Enter username
        username_field = self.wait.until(ec.element_to_be_clickable(self.USERNAME_INPUT))
        username_field.clear()
        username_field.send_keys(username)
        logger.info("Entered username")

        # Enter password
        password_field = self.wait.until(ec.element_to_be_clickable(self.PASSWORD_INPUT))
        password_field.clear()
        password_field.send_keys(password)
        logger.info("Entered password")

        # Click Sign In button
        try:
            sign_in_btn = self.wait.until(ec.element_to_be_clickable(self.SIGN_IN_BUTTON))
            self.safe_click(sign_in_btn, "Sign In button")
        except Exception as e:
            logger.error(f"Sign In button not found or not clickable: {e}")
            self.take_screenshot("Sign In Button Error")
            raise LoginFailedError("Sign In button not found or not clickable")

        # Handle "Already Logged In" popup if present
        try:
            logout_btn = self.wait.until(ec.element_to_be_clickable(self.LOGOUT_BUTTON))
            logger.info("Already Logged In popup detected")

            with allure.step("Detected 'Already Logged In' popup — logging out first"):
                self.safe_click(logout_btn, "Logout button")
                logger.info("Logout button clicked successfully")

            time.sleep(8)  # Wait for logout to complete

            # Click Sign In again after logout
            sign_in_btn = self.wait.until(ec.element_to_be_clickable(self.SIGN_IN_BUTTON))
            sign_in_btn.send_keys(Keys.ENTER)
            logger.info("Pressed Enter on Sign In button after logout")

        except Exception as e:
            logger.error(f"Failed to handle 'Already Logged In' popup: {e}")
            self.take_screenshot("Login Error")
            raise LoginFailedError(f"Login failed: {e}")

        time.sleep(10)  # Wait for the page to load after login