import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time

@allure.step("Logging in with username: {username}")
def Login(driver, username, password, link):
    driver.get(link)
    with allure.step("Enter username"):
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="username"]'))
        ).send_keys(username)

    with allure.step("Enter password"):
        driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="password"]').send_keys(password)

    with allure.step("Click Sign In"):
        sign_in_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]")
        sign_in_btn.click()

    # Handle Already Logged In popup
    try:
        with allure.step("Handle 'Already Logged In' popup if present"):
            logout_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Logout']]"))
            )
            logout_btn.click()
            # Click Sign In again
            sign_in_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign In')]"))
            )
            sign_in_btn.send_keys(Keys.ENTER)
    except TimeoutException:
        with allure.step("No 'Already Logged In' popup detected"):
            pass

    with allure.step("Waiting for login to complete"):
        time.sleep(5)
