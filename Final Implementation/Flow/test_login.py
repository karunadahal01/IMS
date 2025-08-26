#
# #import pytest
# import allure
# import time
# import logging
# import random
# import string
# import pyautogui
# from SeleniumLibrary.keywords import element
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as ec
# from selenium.common.exceptions import WebDriverException
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
#
# import logging
#
# from webdriver_manager.core import driver
#
# import Helper.login_helper
#
# # Logging setup
# logging.basicConfig(level=logging.INFO, format='%(pastime)s - %(levelness)s - %(message)s')
# logger = logging.getLogger(__name__)
#
#
# from Exception.exception import *
# from Helper import *
#
# ########################################### login ###########################################
#
# Helper.login_helper.setup_method()
# Helper.login_helper.teardown_method(driver)
# Helper.login_helper.safe_click(driver, element, description="element")
#
# @allure.step("Login with username: {username}")
# def login(self, username, password, link):
#     driver = self.driver
#     driver.maximize_window()
#     driver.get(link)
#     logger.info(f"Navigated to: {link}")
#
#     username_field = WebDriverWait(driver, 15).until(
#         ec.element_to_be_clickable((By.CSS_SELECTOR, 'input[formcontrolname="username"]'))
#     )
#     username_field.clear()
#     username_field.send_keys(username)
#     logger.info("Entered username")
#
#     password_field = WebDriverWait(driver, 10).until(
#         ec.element_to_be_clickable((By.CSS_SELECTOR, 'input[formcontrolname="password"]'))
#     )
#     password_field.clear()
#     password_field.send_keys(password)
#     logger.info("Entered password")
#
#     # Click the Sign-In button
#     try:
#         sign_in_btn = WebDriverWait(driver, 10).until(
#             ec.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign In')]"))
#         )
#         self.safe_click(sign_in_btn, "Sign In button")
#     except Exception as e:
#         logger.error(f"Sign In button not found or not clickable: {e}")
#         allure.attach(
#             driver.get_screenshot_as_png(),
#             name="Sign In Button Error",
#             attachment_type=allure.attachment_type.PNG
#         )
#         raise LoginFailedError("Sign In button not found or not clickable")
#
#     # Wait for the page to load after login
#     try:
#         logout_btn = WebDriverWait(self.driver, 20).until(
#             ec.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Logout']]"))
#         )
#         logger.info("Already Logged In popup detected")
#
#         # Click Logout button with fallback to JavaScript click
#         try:
#             with allure.step("Detected 'Already Logged In' popup — logging out first"):
#                 self.safe_click(logout_btn, "Logout button")
#                 logger.info("Logout button clicked successfully")
#         except Exception as e:
#             logger.error(f"Failed to click logout button: {e}")
#             allure.attach(
#                 self.driver.get_screenshot_as_png(),
#                 name="Logout Button Error",
#                 attachment_type=allure.attachment_type.PNG
#             )
#             raise LoginFailedError(f"Could not click logout button: {e}")
#
#         logger.info("Logout button clicked successfully")
#         time.sleep(8)  # Wait for logout to complete
#
#         # Wait for the "Sign In" button to be clickable and press Enter
#         sign_in_btn = WebDriverWait(self.driver, 10).until(
#             ec.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign In')]"))
#         )
#
#         # Press Enter on the "Sign In" button
#         sign_in_btn.send_keys(Keys.ENTER)
#         logger.info("Pressed Enter on Sign In button after logout")
#
#     except Exception as e:
#         logger.error(f"Failed to handle 'Already Logged In' popup: {e}")
#         allure.attach(
#             self.driver.get_screenshot_as_png(),
#             name="Login Error",
#             attachment_type=allure.attachment_type.PNG
#         )
#         raise LoginFailedError(f"Login failed: {e}")
#
#     time.sleep(10)  # Wait for the page to load after login

import allure
import time
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from Exception.exception import *
from Helper.login_helper import *

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@allure.step("Login with username: {username}")
def login(driver, username, password, link):
    driver.maximize_window()
    driver.get(link)
    logger.info(f"Navigated to: {link}")

    # Username
    username_field = WebDriverWait(driver, 15).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, 'input[formcontrolname="username"]'))
    )
    username_field.clear()
    username_field.send_keys(username)
    logger.info("Entered username")

    # Password
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
        safe_click(driver, sign_in_btn, "Sign In button")
        time.sleep(20)

    except Exception as e:
        logger.error(f"Sign In button not found or not clickable: {e}")
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Sign In Button Error",
            attachment_type=allure.attachment_type.PNG
        )
        raise LoginFailedError("Sign In button not found or not clickable")


    # Handle Already Logged In popup
    try:
        logout_btn = WebDriverWait(driver, 20).until(
            ec.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Logout']]"))
        )
        logger.info("Already Logged In popup detected")

        try:
            with allure.step("Detected 'Already Logged In' popup — logging out first"):
                safe_click(driver, logout_btn, "Logout button")
                logger.info("Logout button clicked successfully")
        except Exception as e:
            logger.error(f"Failed to click logout button: {e}")
            allure.attach(
                driver.get_screenshot_as_png(),
                name="Logout Button Error",
                attachment_type=allure.attachment_type.PNG
            )
            raise LoginFailedError(f"Could not click logout button: {e}")

        time.sleep(8)  # Wait for logout to complete

        # Re-click Sign In
        sign_in_btn = WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign In')]"))
        )
        sign_in_btn.send_keys(Keys.ENTER)
        logger.info("Pressed Enter on Sign In button after logout")

    except Exception as e:
        logger.error(f"Failed to handle 'Already Logged In' popup: {e}")
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Login Error",
            attachment_type=allure.attachment_type.PNG
        )
        raise LoginFailedError(f"Login failed: {e}")

    time.sleep(10)  # Wait for the page to load after login
