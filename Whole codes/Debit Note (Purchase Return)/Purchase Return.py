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
time.sleep(15)  # Give additional time for page to fully load


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


# Hover over "Purchase Transaction"
purchase_transaction = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Purchase Transaction")))
ActionChains(driver).move_to_element(purchase_transaction).perform()
time.sleep(8)
# Wait for "Sales Tax Invoice" to be visible and click it
debit_note = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Debit Note (Purchase Return)")))
debit_note.click()

print("Clicked 'debit note'")

time.sleep(8)



# Click on the invoiceNO input field
invoiceNO_input = driver.find_element(By.ID, "invoiceNO")
driver.execute_script("arguments[0].removeAttribute('readonly')", invoiceNO_input)  # Remove readonly
invoiceNO_input.click()
invoiceNO_input.send_keys(Keys.ENTER)  # First Enter to load the dropdown

# Wait for options to appear (adjust time or use WebDriverWait if possible)
time.sleep(2)

# Find the body element
body = driver.find_element(By.TAG_NAME, "body")

# Send Enter key to the body
body.send_keys(Keys.ENTER)


#
# # Create a random alphanumeric string of length 8
# def generate_random_refPI(length=8):
#     letters_and_digits = string.ascii_letters + string.digits
#     return ''.join(random.choice(letters_and_digits) for i in range(length))
#
#
# # Generate the random refPI
# random_refPI = generate_random_refPI()
# print(f"Generated RefPI: {random_refPI}")
#
# # Find the input field by ID and input the random refPI
# ref_input = driver.find_element(By.ID, "invoiceNO")
# ref_input.clear()
# ref_input.send_keys(random_refPI)


time.sleep(3)



# For remakrs:
remarks_field = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.ID, "remarksid"))
)

time.sleep(5)

# Clear the field and type the remark
remarks_field.clear()
remarks_field.send_keys("Purchase Return by automation. ")
time.sleep(5)
print("✅ Remarks entered successfully.")

time.sleep(5)
#click on save button
save_button = driver.find_element(By.XPATH, "//button[contains(text(),'SAVE')]")
save_button.click()
time.sleep(10)



# Handle alert ONLY if present
try:
    WebDriverWait(driver, 5).until(EC.alert_is_present())
    alert = driver.switch_to.alert
    alert.accept()
    print("Alert accepted successfully.")
except TimeoutException:
    print("No alert appeared after clicking SAVE.")

# For click on cancel button in print
import pyautogui
# Wait for print preview to open
time.sleep(10)

# Press Escape key to close the print dialog
pyautogui.press('esc')
time.sleep(5)


#  Click on "BACK" button
back_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'BACK')]")))
back_btn.click()
print("Keeping browser open for 15 seconds for observation...")
time.sleep(15)
