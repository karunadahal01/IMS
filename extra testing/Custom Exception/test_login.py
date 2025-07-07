# # from selenium import webdriver
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.support.ui import WebDriverWait, Select
# # from selenium.webdriver.support import expected_conditions as EC
# # from selenium.webdriver.common.keys import Keys
# # from selenium.common.exceptions import TimeoutException
# # from selenium.webdriver.common.action_chains import ActionChains
# # import random
# # import string
# # import time
# #
# # #######################################Custom Exceptions###########################################
# #
# # class InvalidPasswordError(Exception):
# #     """Raised when login fails due to invalid password."""
# #     pass
# #
# # class MissingDataError(Exception):
# #     """Raised when required field data is missing."""
# #     def __init__(self, field_name):
# #         self.message = f"Missing data in required field: {field_name}"
# #         super().__init__(self.message)
# #
# # ########################################################################################################################
# #
# # driver = webdriver.Chrome()
# #
# # def Login(username,password,link):
# #
# #     driver.maximize_window()
# #     driver.get(link)
# #     if not username:
# #         raise MissingDataError("username")
# #     if not password:
# #         raise MissingDataError("password")
# #     try:
# #         # Step 1: Enter credentials and click Sign In
# #         WebDriverWait(driver, 10).until(
# #             EC.presence_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="username"]'))
# #         ).send_keys(username)
# #         driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="password"]').send_keys(password)
# #
# #         sign_in_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]")
# #         sign_in_btn.click()
# #     except Exception:
# #         if "Invalid password" in driver.page_source:
# #             raise InvalidPasswordError("Invalid password provided during login")
# #
# #         # Step 2: Handle "Already Logged In" popup if present
# #     try:
# #         logout_btn = WebDriverWait(driver, 20).until(
# #             EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Logout']]"))
# #         )
# #         print("✓ Already Logged In popup detected")
# #
# #         # Click Logout button
# #         try:
# #                 logout_btn.click()
# #         except Exception:
# #             driver.execute_script("arguments[0].click();", logout_btn)
# #             print("✓ Clicked Logout button")
# #
# #             time.sleep(8)
# #             # Wait for the "Sign In" button to be clickable
# #             sign_in_btn = WebDriverWait(driver, 10).until(
# #                 EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign In')]"))
# #             )
# #
# #             # Press Enter on the "Sign In" button
# #             sign_in_btn.send_keys(Keys.ENTER)
# #             print("✓ Clicked Sign In again after logout")
# #
# #
# #         # Now you should be logged in fresh, add more actions here if needed
# #     finally:
# #         print("Login successfully")
# #         time.sleep(20)
# # Login(username="gedehim917@decodewp.com",password="Tebahal!",link="https://velvet.webredirect.himshang.com.np/#/pages/dashboard")
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import TimeoutException
# import time
#
# import pytest
# ####################################### Custom Exceptions ###########################################
#
# class InvalidPasswordError(Exception):
#     """Raised when login fails due to invalid password."""
#     pass
#
#
# class MissingDataError(Exception):
#     """Raised when required field data is missing."""
#
#     def __init__(self, field_name):
#         self.message = f"Missing data in required field: {field_name}"
#         super().__init__(self.message)
#
#
# #####################################################################################################
#
# driver = webdriver.Chrome()
#
#
# def login(username, password, link):
#     driver.maximize_window()
#     driver.get(link)
#
#     # Check for missing data
#     if not username:
#         raise MissingDataError("username")
#     if not password:
#         raise MissingDataError("password")
#
#     try:
#         # Step 1: Enter credentials and click Sign In
#         print("✓ Filling login form")
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="username"]'))
#         ).send_keys(username)
#
#         driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="password"]').send_keys(password)
#
#         sign_in_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]")
#         sign_in_btn.click()
#
#     except TimeoutException:
#         raise MissingDataError("login form elements not found on the page in time")
#
#     # Step 2: Check if invalid password message appears
#     time.sleep(3)  # Give it time to process login
#     if "Invalid password" in driver.page_source:
#         raise InvalidPasswordError("Invalid Username or Password")
#
#     # Step 3: Handle "Already Logged In" popup if present
#     try:
#         print("✓ Checking if already logged in popup appears")
#         logout_btn = WebDriverWait(driver, 5).until(
#             EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Logout']]"))
#         )
#         print("✓ Already Logged In popup detected, clicking Logout")
#         try:
#             logout_btn.click()
#         except Exception:
#             driver.execute_script("arguments[0].click();", logout_btn)
#             print("✓ Clicked Logout with JS executor")
#
#         # Wait for login page to be ready again
#         WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign In')]"))
#         ).send_keys(Keys.ENTER)
#         print("✓ Clicked Sign In again after logout")
#
#     except TimeoutException:
#         print("✓ No 'already logged in' popup, proceeding normally")
#
#     # Step 4: Confirm logged in by waiting for dashboard element
#     print("✓ Login successful, waiting on dashboard")
#     time.sleep(5)  # Replace with explicit dashboard check if needed
#     print("✓ All done!")
#
#
# #####################################################################################################
#
# # # Example usage
# # def test_login():
# #     login(
# #     username="gedehim917@decodewp.com",
# #     password="Tebahal1!",
# #     link="https://velvet.webredirect.himshang.com.np/#/pages/dashboard"
# # )
# def test_login_invalid_password():
#     with pytest.raises(InvalidPasswordError):
#         login(
#             username="gedehim917@decodewp.com",
#             password="WRONG_PASSWORD",
#             link="https://velvet.webredirect.himshang.com.np/#/pages/dashboard"
#         )
#
# def test_login_missing_password():
#     with pytest.raises(MissingDataError):
#         login(
#             username="gedehim917@decodewp.com",
#             password="",
#             link="https://velvet.webredirect.himshang.com.np/#/pages/dashboard")
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# Custom Exception
class InvalidCredentialsError(Exception):
    """Raised when username or password is invalid."""
    pass

driver = webdriver.Chrome()

def login(username, password, url):
    driver.get(url)

    try:
        # Wait for username field and enter username
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="username"]'))
        ).send_keys(username)

        # Enter password
        driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="password"]').send_keys(password)

        # Click sign in
        driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]").click()

        # Wait a few seconds for error or success message to load
        time.sleep(3)

        # Check if error message is present (adjust selector to your site)
        try:
            error_element = driver.find_element(By.CSS_SELECTOR, ".error-message")  # change selector as needed
            error_text = error_element.text.lower()
            if "invalid" in error_text or "wrong" in error_text:
                raise InvalidCredentialsError("Invalid username or password")
        except:
            # If error element not found, assume login succeeded
            pass

    except TimeoutException:
        print("Login page elements did not load in time")

# Usage example:
try:
    login("wronguser@example.com", "wrongpassword", "https://velvet.webredirect.himshang.com.np/#/pages/dashboard")
except InvalidCredentialsError as e:
    print(e)
else:
    print("Login successful!")

driver.quit()

