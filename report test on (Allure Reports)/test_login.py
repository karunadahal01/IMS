import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
import time

from conftest import driver

##########################################LOG IN###########################################################
@allure.step("Logging in with username: {username} , password: {password} ")
def Login(driver,username,password,link):

    driver.maximize_window()
    driver.get(link)
    try:
     with allure.step("Enter username"):
        # Step 1: Enter credentials and click Sign In
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="username"]'))
        ).send_keys(username)

     with allure.step("Enter password"):

        driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="password"]').send_keys(password)

     with allure.step("Click Sign In button"):
        sign_in_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]")
        sign_in_btn.click()

        # Step 2: Handle "Already Logged In" popup if present
        try:

         with allure.step("Check for 'Already Logged In' popup"):
            logout_btn = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Logout']]"))
            )
            print("✓ Already Logged In popup detected")

            # Click Logout button
            try:
                logout_btn.click()
            except Exception:
                driver.execute_script("arguments[0].click();", logout_btn)
            print("✓ Clicked Logout button")

            time.sleep(8)
            # Wait for the "Sign In" button to be clickable
            sign_in_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign In')]"))
            )

            # Press Enter on the "Sign In" button
            sign_in_btn.send_keys(Keys.ENTER)
            print("✓ Clicked Sign In again after logout")

        except TimeoutException:
            with allure.step("No 'Already Logged In' popup detected - continuing"):
                pass
            # print("ℹ️ No 'Already Logged In' popup detected — continuing without logout")

        # Now you should be logged in fresh, add more actions here if needed

    finally:
        with allure.step("Login successful, waiting before next steps"):
         def pytest_runtest_makereport(item, call):
            outcome = yield
            rep = outcome.get_result()
            if rep.when == "call" and rep.failed:
                driver_fixture = item.funcargs.get("driver", None)
                if driver_fixture:
                    allure.attach(driver_fixture.get_screenshot_as_png(),
                                  name="screenshot_on_failure",
                                  attachment_type=allure.attachment_type.PNG)
            time.sleep(40)
        # print("Login successfully")
        # time.sleep(10)


@allure.title("Test Login to Oracle ERP")
def test_login(driver):
    Login(
        driver,
        username="gedehim917@decodewp.com",
        password="Tebahal1!",
        link="https://velvet.webredirect.himshang.com.np/#/pages/dashboard")
