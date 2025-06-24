
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import random
import string
import time



driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://velvet.webredirect.himshang.com.np/#/pages/dashboard")

try:
    # Step 1: Enter credentials and click Sign In
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="username"]'))
    ).send_keys("gedehim917@decodewp.com")

    driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="password"]').send_keys("Tebahal1!")

    sign_in_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]")
    sign_in_btn.click()

    # Step 2: Handle "Already Logged In" popup if present
    try:
        logout_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Logout']]"))
        )
        print("✓ Already Logged In popup detected")

        # Click Logout button
        try:
            logout_btn.click()
        except Exception:
            driver.execute_script("arguments[0].click();", logout_btn)
        print("✓ Clicked Logout button")

        # # Wait for OK button popup to appear
        # WebDriverWait(driver, 5).until(
        #     EC.visibility_of_element_located((By.XPATH, "//button[.//span[normalize-space()='OK']]"))
        # )
        #
        # # Press Enter key to confirm OK popup
        # body = driver.find_element(By.TAG_NAME, "body")
        # body.send_keys(Keys.ENTER)
        # print("✓ Pressed Enter key to confirm OK")
        #
        # # Small wait for popup to disappear
        # time.sleep(6)

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
   print(" ")



# waiting for dashboard to load
print("Step 5: Waiting for dashboard to load...")
time.sleep(5)  # Give additional time for page to fully load


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
sales_tax_invoice = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Sales Tax Invoice")))
sales_tax_invoice.click()

print("Clicked 'Sales Tax Invoice'")

time.sleep(5)

# sales tax invoice form


# Generate random alphanumeric string (e.g., 8 characters)
# def generate_refno(length=8):
#     return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
#
# # Wait and fill Refno.
# refno_input = WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Refno.']"))
# )
# refno_input.clear()
# refno_input.send_keys(generate_refno())


# Create a random alphanumeric string of length 8
def generate_random_refno(length=8):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))


# Generate the random refno
random_refno = generate_random_refno()
print(f"Generated Refno: {random_refno}")

# Find the input field by ID and input the random refno
refno_input = driver.find_element(By.ID, "refnoInput")
refno_input.clear()
refno_input.send_keys(random_refno)

time.sleep(3)



# 1. Focus on the Customer input field
customer_input = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "customerselectid"))
)

# 2. Click to focus the field
customer_input.click()

customer_input.send_keys(Keys.ENTER)


# 4. Wait for the list to appear (adjust XPath if needed)
# try:
#     first_customer_option = WebDriverWait(driver, 5).until(
#         EC.element_to_be_clickable((
#             By.XPATH, "//*[contains(@class, 'cdk-overlay-container')]//*[contains(@class, 'mat-option')][1]"
#         ))
#     )
#
#     # 5. Click the first item
#     first_customer_option.click()
#     time.sleep(0.5)
#     # 6. Press ENTER to finalize selection
#     customer_input.send_keys(Keys.ENTER)
#     print("✓ Successfully selected first customer from dropdown")
#
# except Exception as e:
#     print(f"⚠️ Could not select customer: {e}")


# 3. Press ENTER to open the dropdown
# customer_input.send_keys(Keys.ENTER)

# 4. Wait briefly for the list to appear
time.sleep(5)  # This gives time for the dropdown to load
# customer_input.send_keys(Keys.ENTER)
# # 5. Press ENTER again to select the first item
# customer_input.send_keys(Keys.ENTER)
body = driver.find_element(By.TAG_NAME, "body")
body.send_keys(Keys.ENTER)



 # Customer account select:






time.sleep(10)
# For remakrs:
remarks_field = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.ID, "remarksid"))
)

# Clear the field and type the remark
remarks_field.clear()
remarks_field.send_keys("This is an automated remark for STI.")
time.sleep(5)
print("✅ Remarks entered successfully.")




def Main_function_productitem(driver, barcode): #, row_index):
            try:
                # --- Barcode Section ---
                barcode_input = driver.find_element(By.ID, "barcodeField")
                barcode_input.clear()
                barcode_input.send_keys(barcode)
                barcode_input.send_keys(Keys.ENTER)

                # --- Quantity Section ---
                quantity = random.randint(10, 100)
                print(f"Generated quantity: {quantity}")

                xpaths = [
                    "//table//tr//td[position()=9]//input",
                    "//input[contains(@name, 'quantity') or contains(@name, 'Quantity')]",
                    "//input[contains(@id, 'quantity') or contains(@id, 'Quantity')]",
                    "//td[contains(@class, 'quantity')]//input",
                    "//table//tbody//tr[1]//td[9]//input",
                ]

                quantity_field = None
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
                print(f"❌ Error in processing barcode '{barcode}': {e}")


Main_function_productitem(driver, "2030")
Main_function_productitem(driver,"2035")




# click on show details


# # Option 1: Click by button text if it's in a <button> or clickable element
# show_detail_btn = driver.find_element(By.XPATH, "//div[contains(text(),'Show Detail') or contains(text(),'Show Detail [F1]')]")
# show_detail_btn.click()

# Option 2: Alternatively send F1 key to the page
body = driver.find_element(By.TAG_NAME, 'body')
body.send_keys(Keys.F1)
time.sleep(5)


# Flat discount
flat_discount = random.randint(1, 50)
print(f"Generated Flat Discount: {flat_discount}%")

# Find the input field and enter the value
input_field = driver.find_element(By.ID, "flatDis1")
input_field.clear()
input_field.send_keys(str(flat_discount)+ Keys.ENTER)
time.sleep(3)
# Find the AFTER button using its visible text


wait = WebDriverWait(driver, 10)
after_button = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[text()='AFTER']"))
)
after_button.click()

# after_button = driver.find_element(By.XPATH, "//button[contains(text(), 'AFTER')]")
# after_button.click()
# click on save button
wait = WebDriverWait(driver, 10)
save_button = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//button[contains(text(), 'SAVE') and contains(@class, 'btn-info')]")))
save_button.click()
time.sleep(5)

# Click on Balance Amount button
balance_amount_button = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//button[contains(text(), 'Balance Amount') and contains(@class, 'btn-info')]")))
balance_amount_button.click()
time.sleep(5)

# CLick on Add button
balance_amount_button = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//button[contains(text(), 'Add') and contains(@class, 'btn-info')]")))
balance_amount_button.click()
time.sleep(5)

#click on save button
# save_button = driver.find_element(By.XPATH, "//button[contains(text(),'SAVE')]")
# save_button.click()
# time.sleep(5)
body = driver.find_element(By.TAG_NAME, 'body')
body.send_keys(Keys.END)
time.sleep(5)


# To view Voucher
# Wait for page to load and click VIEW button
wait = WebDriverWait(driver, 10)
view_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'VIEW')]")))
view_button.click()

time.sleep(2)  # Let the list load, or use explicit wait if needed

actions = ActionChains(driver)
actions.send_keys(Keys.ENTER).perform()

time.sleep(3)  # wait for page to load details after clicking

# click on reset button
reset_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'RESET')]")))
reset_btn.click()

time.sleep(3)
# click on  alert
wait.until(EC.alert_is_present())
alert = driver.switch_to.alert
alert.accept()

# 7. Wait for reset to complete (adjust as needed)
time.sleep(5)

# 8. Click on "BACK" button
back_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'BACK')]")))
back_btn.click()

print("Keeping browser open for 30 seconds for observation...")
time.sleep(30)

