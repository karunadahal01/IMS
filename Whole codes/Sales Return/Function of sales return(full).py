from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import random
import string
import time

driver = webdriver.Chrome()
def Login(username,password,link):

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
            time.sleep(10)

        except TimeoutException:
            print("ℹ️ No 'Already Logged In' popup detected — continuing without logout")

    except Exception as e:
        print(f"An error occurred: {e}")

##########################################################################################################

def sales_return_full(driver):
    # Wait until the menu is loaded
    wait = WebDriverWait(driver, 10)

    # Click on "Transactions"
    try:
        transaction_menu = driver.find_element(By.LINK_TEXT, "Transactions")
        transaction_menu.click()
        print("Clicked on 'Transactions'")
    except Exception as e:
        print("Error clicking 'Transactions':", e)
        time.sleep(10)

    # Hover over "Sales Transaction"
    sales_transaction = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Sales Transaction")))
    ActionChains(driver).move_to_element(sales_transaction).perform()
    time.sleep(5)

    # Wait for "Credit Note (Sales Return)" to be visible and click it
    sales_return = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Credit Note (Sales Return)")))
    sales_return.click()
    print("Clicked 'Credit Note (Sales Return)'")
    time.sleep(5)

    # Click on the Ref Bill No input field
    refbill_input = driver.find_element(By.ID, "refbill")
    driver.execute_script("arguments[0].removeAttribute('readonly')", refbill_input)
    refbill_input.click()
    refbill_input.send_keys(Keys.ENTER)
    time.sleep(2)

    # Find the body element and send Enter key
    body = driver.find_element(By.TAG_NAME, "body")
    body.send_keys(Keys.ENTER)

    # For remarks
    remarks_field = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "remarksid"))
    )
    time.sleep(5)
    remarks_field.clear()
    remarks_field.send_keys("sales Return by automation. ")
    time.sleep(5)
    print("✅ Remarks entered successfully.")

    time.sleep(5)

    # Click on SAVE button
    save_button = driver.find_element(By.XPATH, "//button[contains(text(),'SAVE')]")
    save_button.click()
    time.sleep(10)

    # Click on "BACK" button
    back_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'BACK')]")))
    back_btn.click()
    print("Keeping browser open for 15 seconds for observation...")
    time.sleep(15)

################
Login(username="gedehim917@decodewp.com",
      password="Tebahal1!",
      link="https://velvet.webredirect.himshang.com.np/#/pages/dashboard")

sales_return_full(driver)

