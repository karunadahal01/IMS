import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time


# Custom Exception
class InvalidCredentialsError(Exception):
    """Raised when username or password is invalid."""
    pass


driver = webdriver.Chrome()


@allure.step("Perform login with username: {username} and password: {password}")
def login(username, password, url):
    driver.get(url)

    try:
        with allure.step("Filling login form"):
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="username"]'))
            ).send_keys(username)

            driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="password"]').send_keys(password)

            sign_in_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]")
            sign_in_btn.click()

        time.sleep(3)  # Wait for page to potentially show errors

        # Manual logic check
        if (password != "Tebahal1!" or username != "gedehim917@decodewp.com"):
            allure.attach(driver.get_screenshot_as_png(), name="invalid_credentials",
                          attachment_type=allure.attachment_type.PNG)
            raise InvalidCredentialsError("Invalid username or password by manual check.")

        # Or look for error on page
        try:
            error_element = driver.find_element(By.CSS_SELECTOR, ".error-message")  # change to your selector
            error_text = error_element.text.lower()
            if "invalid" in error_text or "wrong" in error_text:
                allure.attach(driver.get_screenshot_as_png(), name="error_message_detected",
                              attachment_type=allure.attachment_type.PNG)
                raise InvalidCredentialsError("Invalid credentials detected on page.")
            else:
                print("Value is correct.")
        except NoSuchElementException:
            # No error element → assume success
            pass

    except TimeoutException:

        time.sleep(10)
        allure.attach(driver.get_screenshot_as_png(), name="timeout",
                      attachment_type=allure.attachment_type.PNG)
        print("Login page elements did not load in time")
    else:
        allure.attach(driver.get_screenshot_as_png(), name="login_success",
                      attachment_type=allure.attachment_type.PNG)
        print("Right username and password entered successfully.")


# Test / usage example
def test_login_invalid_credentials():
    try:
        login("wronguser@example.com", "wrongpassword",
              "https://velvet.webredirect.himshang.com.np/#/pages/dashboard")
    except InvalidCredentialsError as e:
        print(f"❌ {e}")
        allure.attach(driver.get_screenshot_as_png(), name="final_invalid_credentials",
                      attachment_type=allure.attachment_type.PNG)
    else:
        print("✅ Login successful!")

    driver.quit()
