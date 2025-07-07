import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time


# Custom Exceptions
class LoginFailedError(Exception):
    """Raised when login fails due to invalid credentials or unexpected errors."""


class ProductMasterCreationError(Exception):
    """Raised when product master creation fails."""


driver = webdriver.Chrome()


@allure.step("Perform login with username: {username}")
def Login(username, password, link):
    driver.maximize_window()
    driver.get(link)
    try:
        with allure.step("Entering credentials and clicking Sign In"):
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="username"]'))
            ).send_keys(username)

            driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="password"]').send_keys(password)

            sign_in_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]")
            sign_in_btn.click()

        # Handle already logged in
        try:
            logout_btn = WebDriverWait(driver, 8).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Logout']]"))
            )
            with allure.step("Detected 'Already Logged In' popup — logging out first"):
                logout_btn.click()
                time.sleep(5)
                sign_in_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign In')]"))
                )
                sign_in_btn.send_keys(Keys.ENTER)
                print("✓ Clicked Sign In again after logout")

        except TimeoutException:
            print("ℹ️ No 'Already Logged In' popup detected — continuing.")

        # Check if login actually succeeded by looking for some dashboard element
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Dashboard') or contains(text(),'Masters')]"))
            )
            allure.attach(driver.get_screenshot_as_png(), name="login_success",
                          attachment_type=allure.attachment_type.PNG)
            print("✅ Login successful.")
        except TimeoutException:
            allure.attach(driver.get_screenshot_as_png(), name="login_failed",
                          attachment_type=allure.attachment_type.PNG)
            raise LoginFailedError("Login failed: expected dashboard elements not found.")

    except Exception as e:
        allure.attach(driver.get_screenshot_as_png(), name="login_exception",
                      attachment_type=allure.attachment_type.PNG)
        raise LoginFailedError(f"Login process encountered an error: {e}")



@allure.step("Creating product master for item: {product_item}")
def product_master(driver, product_item, HS_code, unit, item_type,
                   description, category, short_name, purchase_price, sales_price,
                   alt_unit, conversion_factor, barcode_map, barcode_unit):
    wait = WebDriverWait(driver, 10)
    try:
        with allure.step("Navigating to Product Master screen"):
            Master_menu = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Masters")))
            Master_menu.click()

            inventory_info = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Inventory Info")))
            ActionChains(driver).move_to_element(inventory_info).perform()

            product_master_link = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Product Master")))
            product_master_link.click()
            print("✓ Opened Product Master page")

        with allure.step("Starting product creation"):
            add_product_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add Product')]")))
            add_product_btn.click()
            time.sleep(2)
            driver.execute_script("document.body.style.zoom='80%'")

            # Fill item group
            item_group_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='-- Press Enter For Item Group --']")))
            item_group_input.click()
            item_group_input.send_keys(Keys.ENTER, Keys.ENTER)

            # Main group
            main_group_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//ng-select//input[@type='text']")))
            main_group_input.click()
            main_group_input.send_keys(Keys.ENTER, Keys.ENTER)
            wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[normalize-space()='Ok']]"))).click()

            # Fill details
            wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter Item Name']"))).send_keys(product_item, Keys.TAB)
            driver.switch_to.active_element.send_keys(HS_code, Keys.TAB)
            driver.switch_to.active_element.send_keys(Keys.TAB, unit, Keys.TAB, item_type, Keys.TAB)
            driver.switch_to.active_element.send_keys(description, Keys.TAB, category, Keys.TAB, short_name, Keys.TAB)
            wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter Purchase Price']"))).send_keys(purchase_price)
            wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='0']"))).send_keys(sales_price)

            # Alternate Unit
            wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Alternate Unit')]"))).click()
            driver.find_element(By.XPATH, "//select[contains(@class,'ng-pristine')]").click()
            driver.switch_to.active_element.send_keys(alt_unit, Keys.TAB)
            wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='number' and contains(@class, 'ng-valid')]"))).send_keys(conversion_factor)

            # Barcode Mapping
            wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Barcode Mapping')]"))).click()
            driver.find_element(By.XPATH, "//input[@placeholder='Enter Bar Code']").send_keys(barcode_map, Keys.TAB)
            driver.find_element(By.CSS_SELECTOR, 'div.col-2.p-0 select').click()
            driver.switch_to.active_element.send_keys(barcode_unit, Keys.TAB)
            wait.until(EC.element_to_be_clickable((By.ID, "map"))).click()

            # Save
            save_button = driver.find_element(By.XPATH, "//button[contains(text(),'SAVE')]")
            save_button.click()

            # Verify save worked by waiting for some success indicator or timeout
            time.sleep(3)
            allure.attach(driver.get_screenshot_as_png(), name="product_created",
                          attachment_type=allure.attachment_type.PNG)
            print("✅ Product master created successfully.")

    except Exception as e:
        allure.attach(driver.get_screenshot_as_png(), name="product_creation_failed",
                      attachment_type=allure.attachment_type.PNG)
        raise ProductMasterCreationError(f"Failed to create product master: {e}")


# Usage
try:
    Login("gedehim917@decodewp.com", "Tebahal1!", "https://velvet.webredirect.himshang.com.np/#/pages/dashboard")
    product_master(driver,
                   product_item="Testing1",
                   HS_code="123",
                   unit="kg.",
                   item_type="Service Item",
                   description="This is description",
                   category="N/A",
                   short_name="XYZ",
                   purchase_price="120",
                   sales_price="140",
                   alt_unit="Each",
                   conversion_factor="1000",
                   barcode_map="2020",
                   barcode_unit="kg.")
except (LoginFailedError, ProductMasterCreationError) as e:
    print(f"❌ {e}")
finally:
    time.sleep(50)
