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

def login(username, password, url):
    driver.get(url)

    try:
        # Step 1: Enter credentials and click Sign In
        print("✓ Filling login form")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="username"]'))
        ).send_keys(username)

        driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="password"]').send_keys(password)

        sign_in_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]")
        sign_in_btn.click()

        # Wait for potential error message to appear
        time.sleep(3)

        # Simple manual check example (not typical in Selenium)
        if (password != "Tebahal1!" or username != "gedehim917@decodewp.com"):
            raise InvalidCredentialsError("Invalid username or password by manual check.")

        # Or: Try detecting an error message on the page
        try:
            error_element = driver.find_element(By.CSS_SELECTOR, ".error-message")  # Adjust selector
            error_text = error_element.text.lower()
            if "invalid" in error_text or "wrong" in error_text:
                raise InvalidCredentialsError("Invalid username or password detected on page.")
        except NoSuchElementException:
            # No error message element found → assume login is successful
            pass

    except TimeoutException:
        print("Login page elements did not load in time")
    else:
        print("Right username and password entered successfully.")


# Usage example:
try:
    login("wronguser@example.com", "wrong_password", "https://velvet.webredirect.himshang.com.np/#/pages/dashboard")
except InvalidCredentialsError as e:
    print(f"❌ {e}")
else:
    print("✅ Login successful!")

driver.quit()
