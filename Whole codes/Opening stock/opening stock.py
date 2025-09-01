from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import random
import string
import time

driver = webdriver.Chrome()
def login(username,password,link):
    driver.maximize_window()
    driver.get(link)
    try:
        # Step 1: Enter credentials and click Sign In
        WebDriverWait(driver, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="username"]'))
        ).send_keys(username)

        driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="password"]').send_keys(password)

        sign_in_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]")
        sign_in_btn.click()

        # Step 2: Handle "Already Logged In" popup if present
        try:
            logout_btn = WebDriverWait(driver, 20).until(
                ec.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Logout']]"))
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
                ec.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign In')]"))
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


def opening_stock(barcode_stock):
    wait = WebDriverWait(driver, 10)

    # Click on "Transactions"
    try:
        transaction_menu = driver.find_element(By.LINK_TEXT, "Transactions")
        transaction_menu.click()
        print("Clicked on 'Transactions'")
    except Exception as e:
        print("Error clicking 'Transactions':", e)
        time.sleep(10)

    # Hover over "Inventory Movement"
    inventory_movement= wait.until(ec.presence_of_element_located((By.LINK_TEXT, "Inventory Movement")))
    ActionChains(driver).move_to_element(inventory_movement).perform()
    time.sleep(10)

    # Wait for "Opening Stock" to be visible and click it
    opening_stock_link = wait.until(ec.visibility_of_element_located((By.LINK_TEXT, "Opening Stock")))
    opening_stock_link.click()
    print("Clicked 'Opening Stock'")
    time.sleep(10)


login(username="gedehim917@decodewp.com", password="Tebahal1!",
          link="https://velvet.webredirect.himshang.com.np/#/pages/dashboard")

opening_stock(barcode_stock=1)