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

def sales_return_partial(driver, barcode):
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

    # Wait until the checkbox is present and click
    checkbox = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox' and contains(@class, 'ng-pristine')]")))
    checkbox.click()

    # Click on the Ref Bill No input field
    refbill_input = driver.find_element(By.ID, "refbill")
    driver.execute_script("arguments[0].removeAttribute('readonly')", refbill_input)
    refbill_input.click()
    refbill_input.send_keys(Keys.ENTER)
    time.sleep(2)

    # Send Enter to the body
    body = driver.find_element(By.TAG_NAME, "body")
    body.send_keys(Keys.ENTER)

    # For remarks
    remarks_field = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "remarksid"))
    )
    time.sleep(5)
    remarks_field.clear()
    remarks_field.send_keys("Partial sales Return by automation. ")
    time.sleep(5)
    print("✅ Remarks entered successfully.")

    # === Item Entry for single barcode ===
    try:
        barcode_input = driver.find_element(By.ID, "barcodeField")
        barcode_input.clear()
        barcode_input.send_keys(barcode)
        barcode_input.send_keys(Keys.ENTER)

        quantity = random.randint(1, 20)
        print(f"Generated quantity for barcode {barcode}: {quantity}")

        xpaths = [
            "//table//tr//td[position()=9]//input",
            "//input[contains(@name, 'quantity') or contains(@name, 'Quantity')]",
            "//input[contains(@id, 'quantity') or contains(@id, 'Quantity')]",
            "//td[contains(@class, 'quantity')]//input",
            "//table//tbody//tr[1]//td[9]//input",
        ]

        for xpath in xpaths:
            try:
                quantity_field = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                quantity_field.clear()
                quantity_field.send_keys(str(quantity) + Keys.ENTER)
                print(f"✅ Quantity entered for barcode {barcode}")
                time.sleep(2)
                break
            except Exception as e:
                print(f"⚠ Failed with XPath: {xpath} -> {e}")
        else:
            print(f"❌ Could not locate quantity input for barcode {barcode}")

    except Exception as e:
        print(f"❌ Error in processing barcode '{barcode}': {e}")

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

 #############################
Login(username="gedehim917@decodewp.com",
      password="Tebahal1!",
      link="https://velvet.webredirect.himshang.com.np/#/pages/dashboard")
sales_return_partial(driver,
                     "15")
