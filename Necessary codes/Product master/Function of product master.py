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

        except TimeoutException:
            print("ℹ️ No 'Already Logged In' popup detected — continuing without logout")

        # Now you should be logged in fresh, add more actions here if needed

    finally:
        print("Login successfully")
        time.sleep(20)



##########################################################################################################

def product_master(driver,product_item,HS_code,unit,item_type,
                   description,category,short_name,purchase_price,sales_price,
                   alt_unit,conversion_factor,
                   barcode_map,barcode_unit):

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
    add_product = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'Add Product')]")))
    # Click the "Add Product" label
    add_product.click()
    time.sleep(5)

    # zoom out screen
    driver.execute_script("document.body.style.zoom='80%'")
    time.sleep(3)

    # Click on the Item Group input field
    item_group_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='-- Press Enter For Item Group --']")))
    item_group_input.click()
    time.sleep(5)
    # Press Enter on the Item Group field
    item_group_input.send_keys(Keys.ENTER)
    time.sleep(5)

    wait = WebDriverWait(driver, 5)

    # Find and click the main group input field
    main_group_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//ng-select//input[@type='text']")))
    main_group_input.click()
    # Send Enter key to trigger dropdown
    main_group_input.send_keys(Keys.ENTER)
    # Send Enter again to select the first dropdown option
    main_group_input.send_keys(Keys.ENTER)
    main_group_input.send_keys(Keys.ENTER)

    time.sleep(8)

    ok_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[normalize-space()='Ok']]")))
    ok_button.click()

    # Find the input by placeholder and enter item name
    item_name_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter Item Name']")))
    item_name_input.clear()
    item_name_input.send_keys(product_item)

    # Press Tab from keyboard
    driver.switch_to.active_element.send_keys(Keys.TAB)
    time.sleep(5)

    # Enter HSC code
    driver.switch_to.active_element.send_keys(HS_code , Keys.TAB)

    # Click on vatable check box
    wait = WebDriverWait(driver, 10)
    checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox' and contains(@class, 'ng-pristine')]")))
    checkbox.click()
    time.sleep(5)

    # press TAB
    driver.switch_to.active_element.send_keys(Keys.TAB)

    # To select Unit
    driver.switch_to.active_element.send_keys(unit, Keys.TAB)
    time.sleep(5)

    # To select item type
    driver.switch_to.active_element.send_keys(item_type, Keys.TAB)
    time.sleep(5)

    # Description
    driver.switch_to.active_element.send_keys(Keys.TAB)
    driver.switch_to.active_element.send_keys(description, Keys.TAB)
    time.sleep(5)

    # Category
    driver.switch_to.active_element.send_keys(category, Keys.TAB)
    time.sleep(5)

    # Short name
    driver.switch_to.active_element.send_keys(short_name, Keys.TAB)
    time.sleep(5)

    # Purchase price
    price_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='number' and @placeholder='Enter Purchase Price']")))
    price_input.clear()
    price_input.send_keys(purchase_price)
    time.sleep(10)

    # Sales price
    number_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='number' and @placeholder='0']")))
    number_input.clear()
    number_input.send_keys(sales_price)
    time.sleep(10)

    # Go to Alternate Unit tab
    alternate_unit_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='mat-tab-label-content' and normalize-space()='Alternate Unit']")))
    alternate_unit_tab.click()
    time.sleep(8)

    # Select unit: gm
    select_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//select[contains(@class, 'ng-pristine')]")))
    select_element.click()
    driver.switch_to.active_element.send_keys(alt_unit, Keys.TAB)
    print("Unit selected.")

    # Quantity input
    input_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='number' and contains(@class, 'ng-valid')]")))
    input_field.clear()
    input_field.send_keys(conversion_factor)
    time.sleep(5)
    # Barcode Mapping tab
    barcode_mapping = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='mat-tab-label-content' and normalize-space()='Barcode Mapping']")))
    barcode_mapping.click()
    time.sleep(8)

    # Enter Barcode "2020"
    barcode_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter Bar Code']")))
    barcode_input.clear()
    barcode_input.send_keys(barcode_map)
    barcode_input.click()
    time.sleep(5)
    driver.switch_to.active_element.send_keys(Keys.TAB)
    time.sleep(5)

    select_element = driver.find_element(By.CSS_SELECTOR, 'div.col-2.p-0 select')
    select_element.click()
    driver.switch_to.active_element.send_keys(barcode_unit, Keys.TAB)
    time.sleep(5)

    wait = WebDriverWait(driver, 10)
    map_button = wait.until(EC.element_to_be_clickable((By.ID, "map")))
    map_button.click()
    time.sleep(10)

    # Click on save button
    save_button = driver.find_element(By.XPATH, "//button[contains(text(),'SAVE')]")
    save_button.click()
    # Press enter to handle alert of "Do you want to add another product?"
    try:
        body = driver.find_element(By.TAG_NAME, "body")
        body.send_keys(Keys.ENTER)
        time.sleep(10)
    except Exception as e:
        print(f"Error handling 'Do you wanna add another product?' alert: {e}")


#Function call
Login(
      username="gedehim917@decodewp.com",
      password="Tebahal1!",
      link="https://velvet.webredirect.himshang.com.np/#/pages/dashboard")

product_master(driver,
               product_item="Testing1",
               HS_code = "123",
               unit="kg.",
               item_type= "Service Item",
               description= "This is description",
               category="N/A",
               short_name="XYZ",
               purchase_price="120",
               sales_price="140",
               alt_unit="Each",
               conversion_factor="1000",
               barcode_map="2020",
               barcode_unit="kg."


               )
