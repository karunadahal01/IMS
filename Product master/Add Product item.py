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
   print(" ")



# waiting for dashboard to load
print("Step 5: Waiting for dashboard to load...")
time.sleep(15)  # Give additional time for page to fully load


# Wait until the menu is loaded
wait = WebDriverWait(driver, 10)

# Click on "Masters"
try:
    Master_menu = driver.find_element(By.LINK_TEXT, "Masters")
    Master_menu.click()
    print("Clicked on 'Masters'")
except Exception as e:
    print("Error clicking 'Masters':", e)
    time.sleep(10)

# Hover over "inventory_info"
inventory_info = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Inventory Info")))
ActionChains(driver).move_to_element(inventory_info).perform()
time.sleep(5)
# Wait for "Product Master" to be visible and click it
product_master = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Product Master")))
product_master.click()

print("Clicked 'Product Master'")

time.sleep(5)

# Click on "Add Product" button
back_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add Product')]")))
back_btn.click()
time.sleep(10)

wait = WebDriverWait(driver, 10)
add_product = wait.until(EC.element_to_be_clickable((
    By.XPATH, "//label[contains(text(), 'Add Product')]"
)))
# Click the "Add Product" label
add_product.click()
time.sleep(5)
#zoom out screen
driver.execute_script("document.body.style.zoom='80%'")

time.sleep(3)

#  Click on the Item Group input field
item_group_input = wait.until(EC.element_to_be_clickable((
    By.XPATH, "//input[@placeholder='-- Press Enter For Item Group --']"
)))
item_group_input.click()
time.sleep(5)
#  Press Enter on the Item Group field
item_group_input.send_keys(Keys.ENTER)
time.sleep(5)



wait = WebDriverWait(driver, 5)

#  Find and click the main group input field
main_group_input = wait.until(EC.element_to_be_clickable((
    By.XPATH, "//ng-select//input[@type='text']"
)))
main_group_input.click()

#  Send Enter key to trigger dropdown
main_group_input.send_keys(Keys.ENTER)

#  Send Enter again to select the first dropdown option
main_group_input.send_keys(Keys.ENTER)



main_group_input.send_keys(Keys.ENTER)

time.sleep(8)

ok_button = wait.until(EC.element_to_be_clickable((
    By.XPATH, "//button[.//span[normalize-space()='Ok']]"
)))
ok_button.click()


# Find the input by placeholder and enter item name
item_name_input = wait.until(EC.element_to_be_clickable((
    By.XPATH, "//input[@placeholder='Enter Item Name']"
)))
item_name_input.clear()
item_name_input.send_keys("Test Item1")

#Press Tab from keyboard
driver.switch_to.active_element.send_keys(Keys.TAB)


time.sleep(5)
# Enter HSC code
driver.switch_to.active_element.send_keys("123", Keys.TAB)

# CLick on vatable check box

# Wait until the checkbox is present
wait = WebDriverWait(driver, 10)
checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox' and contains(@class, 'ng-pristine')]")))

# Click the checkbox
checkbox.click()
time.sleep(5)
#press TAB
driver.switch_to.active_element.send_keys(Keys.TAB)

# To select Unit

driver.switch_to.active_element.send_keys("kg.", Keys.TAB)
time.sleep(5)
# To select item type
driver.switch_to.active_element.send_keys("Service Item", Keys.TAB)
time.sleep(5)
# Description
driver.switch_to.active_element.send_keys(Keys.TAB)
driver.switch_to.active_element.send_keys("This is description", Keys.TAB)
time.sleep(5)
# Category
driver.switch_to.active_element.send_keys("N/A", Keys.TAB)
time.sleep(5)
# Shoort name
driver.switch_to.active_element.send_keys("PTI", Keys.TAB)
time.sleep(5)

# Purchase price
# Find the input field by placeholder
price_input = wait.until(EC.element_to_be_clickable((
    By.XPATH, "//input[@type='number' and @placeholder='Enter Purchase Price']"
)))

# Clear existing value (if any) and enter 130
price_input.clear()
price_input.send_keys("130")

time.sleep(10)

# sales price
# Locate the input by placeholder
number_input = wait.until(EC.element_to_be_clickable((
    By.XPATH, "//input[@type='number' and @placeholder='0']"
)))

# Clear existing value and enter 160
number_input.clear()
number_input.send_keys("160")
time.sleep(10)

# Go In Alterntive unit
# Find and click the tab by its text
alternate_unit_tab = wait.until(EC.element_to_be_clickable((
    By.XPATH, "//div[@class='mat-tab-label-content' and normalize-space()='Alternate Unit']"
)))
alternate_unit_tab.click()
time.sleep(8)

# Find and click the select unit :gm

# Wait for the <select> element to be clickable (using class)
select_element = wait.until(EC.element_to_be_clickable((
    By.XPATH, "//select[contains(@class, 'ng-pristine')]"
)))
# Click the select field to open the dropdown
select_element.click()
driver.switch_to.active_element.send_keys("gm", Keys.TAB)
print("Unit selected.")

# Wait for the input field using class
input_field = wait.until(EC.element_to_be_clickable((
    By.XPATH, "//input[@type='number' and contains(@class, 'ng-valid')]"
)))

# Clear any existing value
input_field.clear()

# Enter 1000
input_field.send_keys("1000")


# Find and click the tab by its text
barcode_mapping = wait.until(EC.element_to_be_clickable((
    By.XPATH, "//div[@class='mat-tab-label-content' and normalize-space()='Barcode Mapping']"
)))
barcode_mapping.click()
time.sleep(8)


# ----- Step 1: Enter Barcode -----
barcode_input = wait.until(EC.presence_of_element_located(
    (By.XPATH, "//input[@placeholder='Enter Bar Code']")
))
barcode_input.clear()
barcode_input.send_keys("2020")
barcode_input.click()
time.sleep(5)
driver.switch_to.active_element.send_keys(Keys.TAB)


time.sleep(5)
select_element = driver.find_element(By.CSS_SELECTOR, 'div.col-2.p-0 select')
select_element.click()
driver.switch_to.active_element.send_keys("gm", Keys.TAB)
time.sleep(5)

wait = WebDriverWait(driver, 10)
map_button = wait.until(EC.element_to_be_clickable((By.ID, "map")))

# Click the button
map_button.click()
time.sleep(10)


# Barcdode for "kg"

# ----- Step 1: Enter Barcode -----
barcode_input = wait.until(EC.presence_of_element_located(
    (By.XPATH, "//input[@placeholder='Enter Bar Code']")
))
barcode_input.clear()
barcode_input.send_keys("2021")
barcode_input.click()
time.sleep(5)
driver.switch_to.active_element.send_keys(Keys.TAB)


time.sleep(5)
select_element = driver.find_element(By.CSS_SELECTOR, 'div.col-2.p-0 select')
select_element.click()
driver.switch_to.active_element.send_keys("kg", Keys.TAB)
time.sleep(5)

wait = WebDriverWait(driver, 10)
map_button = wait.until(EC.element_to_be_clickable((By.ID, "map")))

# Click the button
map_button.click()
time.sleep(10)
# driver.switch_to.active_element.send_keys(Keys.TAB)

#click on save button
save_button = driver.find_element(By.XPATH, "//button[contains(text(),'SAVE')]")
save_button.click()

print("Keeping browser open for observation...")
time.sleep(40)


