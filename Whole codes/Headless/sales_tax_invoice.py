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



#########################################################################################
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")          # Run in headless mode
options.add_argument("--no-sandbox")        # For some environments
options.add_argument("--disable-dev-shm-usage")  # Prevents resource issues
options.add_argument("--window-size=1920,1080")  # Optional: set window size
###########################################################################################



driver = webdriver.Chrome(options=options)
def Login(username,password,link):
    #driver.maximize_window()
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
Login(username="gedehim917@decodewp.com",password="Tebahal1!",link="https://velvet.webredirect.himshang.com.np/#/pages/dashboard")



def sales_tax_invoice(driver, barcode_sales):
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

    # Wait for "Sales Tax Invoice" to be visible and click it
    sales_tax_invoice_link = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Sales Tax Invoice")))
    sales_tax_invoice_link.click()
    print("Clicked 'Sales Tax Invoice'")
    time.sleep(5)

    # Generate random refno
    def generate_random_refno(length=8):
        letters_and_digits = string.ascii_letters + string.digits
        return ''.join(random.choice(letters_and_digits) for i in range(length))

    random_refno = generate_random_refno()
    print(f"Generated Refno: {random_refno}")

    refno_input = driver.find_element(By.ID, "refnoInput")
    refno_input.clear()
    refno_input.send_keys(random_refno)
    time.sleep(3)

    # Focus on Customer input field
    customer_input = wait.until(EC.element_to_be_clickable((By.ID, "customerselectid")))
    customer_input.click()
    customer_input.send_keys(Keys.ENTER)
    time.sleep(5)

    # Press ENTER on body to confirm selection
    body = driver.find_element(By.TAG_NAME, "body")
    body.send_keys(Keys.ENTER)

    time.sleep(10)

    # Remarks
    remarks_field = wait.until(EC.element_to_be_clickable((By.ID, "remarksid")))
    remarks_field.clear()
    remarks_field.send_keys("This is an automated remark for STI.")
    time.sleep(5)
    print("✅ Remarks entered successfully.")

    # --- Barcode Section ---
    try:
        barcode_input = driver.find_element(By.ID, "barcodeField")
        barcode_input.clear()
        barcode_input.send_keys(barcode_sales)
        barcode_input.send_keys(Keys.ENTER)

        # --- Quantity Section ---
        quantity = random.randint(10, 80)
        print(f"Generated quantity: {quantity}")

        xpaths = [
            "//table//tr//td[position()=9]//input",
            "//input[contains(@name, 'quantity') or contains(@name, 'Quantity')]",
            "//input[contains(@id, 'quantity') or contains(@id, 'Quantity')]",
            "//td[contains(@class, 'quantity')]//input",
            "//table//tbody//tr[1]//td[9]//input",
        ]

        # quantity_field = None
        for xpath in xpaths:
            try:
                quantity_field = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, xpath))
                )
                quantity_field.clear()
                quantity_field.send_keys(str(quantity) + Keys.ENTER)
                print("✅ Quantity entered and Enter key pressed.")
                time.sleep(2)
                break
            except Exception as e:
                print(f"⚠ Failed with XPath: {xpath} -> {e}")
        else:
            print("❌ Could not locate the quantity input field.")

    except Exception as e:
        print(f"❌ Error in processing barcode '{barcode_sales}': {e}")

    # Show Details
    body = driver.find_element(By.TAG_NAME, 'body')
    body.send_keys(Keys.F1)
    time.sleep(5)

    # Flat Discount
    flat_discount = random.randint(1, 50)
    print(f"Generated Flat Discount: {flat_discount}%")

    input_field = driver.find_element(By.ID, "flatDis1")
    input_field.clear()
    input_field.send_keys(str(flat_discount) + Keys.ENTER)
    time.sleep(3)

    # AFTER button
    after_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='AFTER']"))
    )
    after_button.click()

    # SAVE button
    save_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(text(), 'SAVE') and contains(@class, 'btn-info')]")))
    save_button.click()
    time.sleep(5)

    # Balance Amount
    balance_amount_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(text(), 'Balance Amount') and contains(@class, 'btn-info')]")))
    balance_amount_button.click()
    time.sleep(5)

    # Add button
    add_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(text(), 'Add') and contains(@class, 'btn-info')]")))
    add_button.click()
    time.sleep(5)

    # Scroll to end
    body = driver.find_element(By.TAG_NAME, 'body')
    body.send_keys(Keys.END)
    time.sleep(10)

    # View Voucher
    view_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'VIEW')]")))
    view_button.click()
    time.sleep(2)

    actions = ActionChains(driver)
    actions.send_keys(Keys.ENTER).perform()
    time.sleep(5)

    # Reset button
    reset_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'RESET')]")))
    reset_btn.click()
    time.sleep(5)

    # Accept alert
    wait.until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()
    time.sleep(5)

    # Back button
    back_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'BACK')]")))
    back_btn.click()
    print(driver.title)  # Just to verify
    driver.quit()
    print("flow completed.")

sales_tax_invoice(driver,
                  barcode_sales=2020)

print("Keeping browser open for 30 seconds for observation...")
time.sleep(30)