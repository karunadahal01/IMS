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

        except TimeoutException:
            print("ℹ️ No 'Already Logged In' popup detected — continuing without logout")

        # Now you should be logged in fresh, add more actions here if needed

    finally:
        print("Login successfully")
        time.sleep(10)




def customer():
    wait = WebDriverWait(driver, 10)

    # Click on "Utilities"
    try:
        Utilities_menu = driver.find_element(By.LINK_TEXT, "Utilities")
        Utilities_menu.click()
        print("Clicked on 'Utilities'")
    except Exception as e:
        print("Error clicking 'Utilities':", e)
        time.sleep(10)

    # Click on "Migration"
    try:
        migration_menu = driver.find_element(By.LINK_TEXT, "Migration")
        migration_menu.click()
        print("Clicked on 'Migration'")
    except Exception as e:
        print("Error clicking 'Migration':", e)
        time.sleep(10)

    # Click on "Master Migration"
    try:
        master_migration_menu = driver.find_element(By.LINK_TEXT, "Master Migration")
        master_migration_menu.click()
        time.sleep(4)
        body = driver.find_element(By.TAG_NAME, 'body')
        # Click the body
        body.click()
        print("Clicked on 'Master Migration'")
    except Exception as e:
        print("Error clicking 'Master Migration':", e)
        time.sleep(10)

     # CLick on upload sheet
    try:
       # Wait until the element is clickable
       upload_sheet_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.nav-link[href="#upload-sheet"]'))
       )
       upload_sheet_link.click()
       print("Clicked on 'Upload Sheet'")
    except Exception as e:
        print("Error clicking 'Upload Sheet':", e)
        time.sleep(10)


     # select customer master
    try:
        # # Locate the select element (by name in this case)
        # select_element = driver.find_element(By.NAME, "selectedMaster")
        #
        # # Wrap the element with Select class
        # dropdown = Select(select_element)
        #
        # # Select by visible text
        # dropdown.select_by_visible_text("Customer Master")
        #
        # # Optional: wait or continue other actions
        time.sleep(10)
        body = driver.find_element(By.TAG_NAME, 'body')
        actions = ActionChains(driver)
        #actions.click(body).send_keys(Keys.TAB).send_keys(Keys.TAB).perform()
        actions.click(body).send_keys(Keys.TAB).perform()
        driver.switch_to.active_element.send_keys("Customer Master")
        # select_element = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.NAME, "selectedMaster"))
        # )
        #
        # # Create Select object
        # select = Select(select_element)

        # Select the option with visible text "Customer Master"
        #select.select_by_visible_text("Customer Master")

    except Exception as e:
        print("Error selecting 'Customer Master':", e)
        time.sleep(10)

    #SElecting file
    time.sleep(3)

    # Locate the file input element
    file_input = driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')

    # # Click on it (optional)
    # file_input.click()

    # Press Enter key (simulate)
    file_input.send_keys(Keys.ENTER)
    file_input.send_keys("Downloads/Customer Master Sample.xlsx")

    # Optional: Close the browser
    time.sleep(3)


Login(username="gedehim917@decodewp.com",password="Tebahal1!",link="https://velvet.webredirect.himshang.com.np/#/pages/dashboard")
customer()

