from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
#import random
#import string
import time

driver = webdriver.Chrome()


def Login(username, password, link):
    driver.maximize_window()
    driver.get(link)
    try:
        # Step 1: Enter credentials and click Sign In
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="username"]'))
        ).send_keys(username)

        driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="password"]').send_keys(password)

        sign_in_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]")
        sign_in_btn.click()

        # Step 2: Handle "Already Logged In" popup if present
        try:
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
            print("ℹ️ No 'Already Logged In' popup detected — continuing without logout")

        # Now you should be logged in fresh, add more actions here if needed

    finally:
        print("Login successfully")
        time.sleep(10)

def sales_tax_invoice():
    # Navigate to Reports
    try:
        # wait = WebDriverWait(driver, 10)
        # reports_menu = wait.until(EC.element_to_be_clickable(
        #     (By.XPATH, "//a[@title='Reports']//span[contains(text(),'Reports')]")))
        # ActionChains(driver).move_to_element(reports_menu).perform()
        reports_menu = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//a[@title='Reports']"))
        )

        # Hover
        reports_menu.click()
        reports_menu.click()
        reports_menu.click()
        #ActionChains(driver).move_to_element(reports_menu).perform()
        time.sleep(10)  # give time for submenu to appear

    except Exception as e:
        print(f"Error navigating to Reports: {e}")

##############navigation to Sales Report
    try:
            wait = WebDriverWait(driver, 10)
            sales_report = wait.until(EC.visibility_of_element_located(
                (By.XPATH, "//span[text()='Sales Report']")))
            ActionChains(driver).move_to_element(sales_report).click().perform()
            time.sleep(10)
    except Exception as e:
            print(f"Error clicking Sales Report: {e}")




Login(username="gedehim917@decodewp.com", password="Tebahal1!",
              link="https://velvet.webredirect.himshang.com.np/#/pages/dashboard")
sales_tax_invoice()
