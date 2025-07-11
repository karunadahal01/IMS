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
import allure
# import pytest
from allure_commons.types import AttachmentType
# import os

driver = webdriver.Chrome()

#
# def take_screenshot(driver, name):
#     """Take screenshot and attach to Allure report"""
#     try:
#         screenshot = driver.get_screenshot_as_png()
#         allure.attach(screenshot, name=name, attachment_type=AttachmentType.PNG)
#     except Exception as e:
#         print(f"Failed to take screenshot: {e}")
#
#
# def allure_step_with_screenshot(step_name, driver_instance=None):
#     """Decorator to add Allure step with screenshot on failure"""
#
#     def decorator(func):
#         def wrapper(*args, **kwargs):
#             with allure.step(step_name):
#                 try:
#                     result = func(*args, **kwargs)
#                     return result
#                 except Exception as e:
#                     if driver_instance:
#                         take_screenshot(driver_instance, f"Error_{step_name}")
#                     raise e
#
#         return wrapper
#
#     return decorator


##########################################LOG IN###########################################################

@allure.feature("Authentication")
@allure.story("User Login")
@allure.title("Login to Application")
@allure.description("This test performs login to the application with provided credentials")
def Login(username, password, link):
    global driver

    with allure.step(f"Navigate to application URL: {link}"):
        driver.maximize_window()
        driver.get(link)
        # take_screenshot(driver, "Login_Page_Loaded")

    try:
        with allure.step("Enter username"):
            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="username"]'))
            )
            username_field.send_keys(username)
            # allure.attach(username, name="Username", attachment_type=AttachmentType.TEXT)
            # take_screenshot(driver, "Username_Entered")

        with allure.step("Enter password"):
            password_field = driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="password"]')
            password_field.send_keys(password)
            # take_screenshot(driver, "Password_Entered")

        with allure.step("Click Sign In button"):
            sign_in_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]")
            sign_in_btn.click()
           # take_screenshot(driver, "Sign_In_Clicked")

        with allure.step("Handle 'Already Logged In' popup if present"):
            try:
                logout_btn = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Logout']]"))
                )
                print("✓ Already Logged In popup detected")
                #take_screenshot(driver, "Already_Logged_In_Popup")

                try:
                    logout_btn.click()
                except Exception:
                    driver.execute_script("arguments[0].click();", logout_btn)
                print("✓ Clicked Logout button")
               # take_screenshot(driver, "Logout_Clicked")

                time.sleep(8)
                sign_in_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign In')]"))
                )
                sign_in_btn.send_keys(Keys.ENTER)
                print("✓ Clicked Sign In again after logout")
                #take_screenshot(driver, "Sign_In_After_Logout")

            except TimeoutException:
                print("ℹ️ No 'Already Logged In' popup detected — continuing without logout")

    except Exception as e:
        # take_screenshot(driver, "Login_Error")
        # allure.attach(str(e), name="Login Error Details", attachment_type=AttachmentType.TEXT)
        raise e
    finally:
        print("Login successfully")
       # take_screenshot(driver, "Login_Success")
        time.sleep(10)


########################################## PRODUCT MASTER ###########################################################

@allure.feature("Inventory Management")
@allure.story("Product Master")
@allure.title("Create Product Master")
@allure.description("This test creates a new product in the Product Master module")
def product_master(driver, product_item, HS_code, unit, item_type,
                   description, category, short_name, purchase_price, sales_price,
                   alt_unit, conversion_factor, barcode_map, barcode_unit):
    wait = WebDriverWait(driver, 10)

    with allure.step("Navigate to Masters menu"):
        try:
            Master_menu = driver.find_element(By.LINK_TEXT, "Masters")
            Master_menu.click()
            print("Clicked on 'Masters'")
           # take_screenshot(driver, "Masters_Menu_Clicked")
        except Exception as e:
            #take_screenshot(driver, "Masters_Menu_Error")
            raise e

    with allure.step("Navigate to Product Master"):
        try:
            inventory_info = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Inventory Info")))
            ActionChains(driver).move_to_element(inventory_info).perform()
            time.sleep(5)
            #take_screenshot(driver, "Inventory_Info_Hovered")

            product_master_link = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Product Master")))
            product_master_link.click()
            print("Clicked 'Product Master'")
            time.sleep(5)
           # take_screenshot(driver, "Product_Master_Opened")
        except Exception as e:
           # take_screenshot(driver, "Product_Master_Navigation_Error")
            raise e

    with allure.step("Click Add Product button"):
        try:
            back_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add Product')]")))
            back_btn.click()
            time.sleep(10)
           # take_screenshot(driver, "Add_Product_Button_Clicked")
        except Exception as e:
           # take_screenshot(driver, "Add_Product_Button_Error")
            raise e

    with allure.step("Select Add Product option"):
        try:
            add_product = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'Add Product')]")))
            add_product.click()
            time.sleep(5)
           # take_screenshot(driver, "Add_Product_Option_Selected")
        except Exception as e:
           # take_screenshot(driver, "Add_Product_Option_Error")
            raise e

    with allure.step("Set zoom level and configure Item Group"):
        try:
            driver.execute_script("document.body.style.zoom='80%'")
            time.sleep(3)

            item_group_input = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='-- Press Enter For Item Group --']")))
            item_group_input.click()
            time.sleep(5)
            item_group_input.send_keys(Keys.ENTER)
            time.sleep(5)
            #take_screenshot(driver, "Item_Group_Configured")
        except Exception as e:
           # take_screenshot(driver, "Item_Group_Error")
            raise e

    with allure.step("Configure Main Group"):
        try:
            main_group_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//ng-select//input[@type='text']")))
            main_group_input.click()
            main_group_input.send_keys(Keys.ENTER)
            main_group_input.send_keys(Keys.ENTER)
            main_group_input.send_keys(Keys.ENTER)
            time.sleep(8)

            ok_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[normalize-space()='Ok']]")))
            ok_button.click()
           # take_screenshot(driver, "Main_Group_Configured")
        except Exception as e:
           # take_screenshot(driver, "Main_Group_Error")
            raise e

    with allure.step(f"Enter product details - Item Name: {product_item}"):
        try:
            item_name_input = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter Item Name']")))
            item_name_input.clear()
            item_name_input.send_keys(product_item)
            allure.attach(product_item, name="Product Item Name", attachment_type=AttachmentType.TEXT)

            driver.switch_to.active_element.send_keys(Keys.TAB)
            time.sleep(5)
           # take_screenshot(driver, "Product_Name_Entered")
        except Exception as e:
           # take_screenshot(driver, "Product_Name_Error")
            raise e

    with allure.step(f"Enter HSC code: {HS_code}"):
        try:
            driver.switch_to.active_element.send_keys(HS_code, Keys.TAB)
            allure.attach(HS_code, name="HS Code", attachment_type=AttachmentType.TEXT)
            #take_screenshot(driver, "HS_Code_Entered")
        except Exception as e:
            #take_screenshot(driver, "HS_Code_Error")
            raise e

    with allure.step("Configure VAT checkbox and other details"):
        try:
            checkbox = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox' and contains(@class, 'ng-pristine')]")))
            checkbox.click()
            time.sleep(5)

            driver.switch_to.active_element.send_keys(Keys.TAB)
            driver.switch_to.active_element.send_keys(unit, Keys.TAB)
            time.sleep(5)
            driver.switch_to.active_element.send_keys(item_type, Keys.TAB)
            time.sleep(5)
            driver.switch_to.active_element.send_keys(Keys.TAB)
            driver.switch_to.active_element.send_keys(description, Keys.TAB)
            time.sleep(5)
            driver.switch_to.active_element.send_keys(category, Keys.TAB)
            time.sleep(5)
            driver.switch_to.active_element.send_keys(short_name, Keys.TAB)
            time.sleep(5)
            #take_screenshot(driver, "Basic_Details_Entered")
        except Exception as e:
            #take_screenshot(driver, "Basic_Details_Error")
            raise e

    with allure.step(f"Enter pricing - Purchase: {purchase_price}, Sales: {sales_price}"):
        try:
            price_input = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//input[@type='number' and @placeholder='Enter Purchase Price']")))
            price_input.clear()
            price_input.send_keys(purchase_price)
            time.sleep(10)

            number_input = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='number' and @placeholder='0']")))
            number_input.clear()
            number_input.send_keys(sales_price)
            time.sleep(10)

            allure.attach(f"Purchase: {purchase_price}, Sales: {sales_price}",
                          name="Pricing Details", attachment_type=AttachmentType.TEXT)
            #take_screenshot(driver, "Pricing_Entered")
        except Exception as e:
            #take_screenshot(driver, "Pricing_Error")
            raise e

    with allure.step("Configure Alternate Unit"):
        try:
            alternate_unit_tab = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[@class='mat-tab-label-content' and normalize-space()='Alternate Unit']")))
            alternate_unit_tab.click()
            time.sleep(8)

            select_element = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//select[contains(@class, 'ng-pristine')]")))
            select_element.click()
            driver.switch_to.active_element.send_keys(alt_unit, Keys.TAB)
            print("Unit selected.")

            input_field = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='number' and contains(@class, 'ng-valid')]")))
            input_field.clear()
            input_field.send_keys(conversion_factor)
            time.sleep(5)
            #take_screenshot(driver, "Alternate_Unit_Configured")
        except Exception as e:
            #take_screenshot(driver, "Alternate_Unit_Error")
            raise e

    with allure.step(f"Configure Barcode Mapping - Barcode: {barcode_map}"):
        try:
            barcode_mapping = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[@class='mat-tab-label-content' and normalize-space()='Barcode Mapping']")))
            barcode_mapping.click()
            time.sleep(8)

            barcode_input = wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter Bar Code']")))
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

            map_button = wait.until(EC.element_to_be_clickable((By.ID, "map")))
            map_button.click()
            time.sleep(10)

            allure.attach(barcode_map, name="Barcode", attachment_type=AttachmentType.TEXT)
            #take_screenshot(driver, "Barcode_Mapped")
        except Exception as e:
            #take_screenshot(driver, "Barcode_Mapping_Error")
            raise e

    with allure.step("Save Product"):
        try:
            save_button = driver.find_element(By.XPATH, "//button[contains(text(),'SAVE')]")
            save_button.click()
            #take_screenshot(driver, "Product_Saved")

            # Verify product creation success
            assert "product" in driver.current_url.lower() or "success" in driver.page_source.lower(), "Product creation may have failed"

        except Exception as e:
            #take_screenshot(driver, "Product_Save_Error")
            raise e

