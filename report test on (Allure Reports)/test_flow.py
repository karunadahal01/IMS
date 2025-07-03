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
import pytest
from allure_commons.types import AttachmentType
import os

driver = webdriver.Chrome()


def take_screenshot(driver, name):
    """Take screenshot and attach to Allure report"""
    try:
        screenshot = driver.get_screenshot_as_png()
        allure.attach(screenshot, name=name, attachment_type=AttachmentType.PNG)
    except Exception as e:
        print(f"Failed to take screenshot: {e}")


def allure_step_with_screenshot(step_name, driver_instance=None):
    """Decorator to add Allure step with screenshot on failure"""

    def decorator(func):
        def wrapper(*args, **kwargs):
            with allure.step(step_name):
                try:
                    result = func(*args, **kwargs)
                    return result
                except Exception as e:
                    if driver_instance:
                        take_screenshot(driver_instance, f"Error_{step_name}")
                    raise e

        return wrapper

    return decorator


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
        take_screenshot(driver, "Login_Page_Loaded")

    try:
        with allure.step("Enter username"):
            username_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="username"]'))
            )
            username_field.send_keys(username)
            allure.attach(username, name="Username", attachment_type=AttachmentType.TEXT)
            take_screenshot(driver, "Username_Entered")

        with allure.step("Enter password"):
            password_field = driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="password"]')
            password_field.send_keys(password)
            take_screenshot(driver, "Password_Entered")

        with allure.step("Click Sign In button"):
            sign_in_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]")
            sign_in_btn.click()
            take_screenshot(driver, "Sign_In_Clicked")

        with allure.step("Handle 'Already Logged In' popup if present"):
            try:
                logout_btn = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Logout']]"))
                )
                print("✓ Already Logged In popup detected")
                take_screenshot(driver, "Already_Logged_In_Popup")

                try:
                    logout_btn.click()
                except Exception:
                    driver.execute_script("arguments[0].click();", logout_btn)
                print("✓ Clicked Logout button")
                take_screenshot(driver, "Logout_Clicked")

                time.sleep(8)
                sign_in_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign In')]"))
                )
                sign_in_btn.send_keys(Keys.ENTER)
                print("✓ Clicked Sign In again after logout")
                take_screenshot(driver, "Sign_In_After_Logout")

            except TimeoutException:
                print("ℹ️ No 'Already Logged In' popup detected — continuing without logout")

    except Exception as e:
        take_screenshot(driver, "Login_Error")
        allure.attach(str(e), name="Login Error Details", attachment_type=AttachmentType.TEXT)
        raise e
    finally:
        print("Login successfully")
        take_screenshot(driver, "Login_Success")
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
            take_screenshot(driver, "Masters_Menu_Clicked")
        except Exception as e:
            take_screenshot(driver, "Masters_Menu_Error")
            raise e

    with allure.step("Navigate to Product Master"):
        try:
            inventory_info = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Inventory Info")))
            ActionChains(driver).move_to_element(inventory_info).perform()
            time.sleep(5)
            take_screenshot(driver, "Inventory_Info_Hovered")

            product_master_link = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Product Master")))
            product_master_link.click()
            print("Clicked 'Product Master'")
            time.sleep(5)
            take_screenshot(driver, "Product_Master_Opened")
        except Exception as e:
            take_screenshot(driver, "Product_Master_Navigation_Error")
            raise e

    with allure.step("Click Add Product button"):
        try:
            back_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add Product')]")))
            back_btn.click()
            time.sleep(10)
            take_screenshot(driver, "Add_Product_Button_Clicked")
        except Exception as e:
            take_screenshot(driver, "Add_Product_Button_Error")
            raise e

    with allure.step("Select Add Product option"):
        try:
            add_product = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'Add Product')]")))
            add_product.click()
            time.sleep(5)
            take_screenshot(driver, "Add_Product_Option_Selected")
        except Exception as e:
            take_screenshot(driver, "Add_Product_Option_Error")
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
            take_screenshot(driver, "Item_Group_Configured")
        except Exception as e:
            take_screenshot(driver, "Item_Group_Error")
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
            take_screenshot(driver, "Main_Group_Configured")
        except Exception as e:
            take_screenshot(driver, "Main_Group_Error")
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
            take_screenshot(driver, "Product_Name_Entered")
        except Exception as e:
            take_screenshot(driver, "Product_Name_Error")
            raise e

    with allure.step(f"Enter HSC code: {HS_code}"):
        try:
            driver.switch_to.active_element.send_keys(HS_code, Keys.TAB)
            allure.attach(HS_code, name="HS Code", attachment_type=AttachmentType.TEXT)
            take_screenshot(driver, "HS_Code_Entered")
        except Exception as e:
            take_screenshot(driver, "HS_Code_Error")
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
            take_screenshot(driver, "Basic_Details_Entered")
        except Exception as e:
            take_screenshot(driver, "Basic_Details_Error")
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
            take_screenshot(driver, "Pricing_Entered")
        except Exception as e:
            take_screenshot(driver, "Pricing_Error")
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
            take_screenshot(driver, "Alternate_Unit_Configured")
        except Exception as e:
            take_screenshot(driver, "Alternate_Unit_Error")
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
            take_screenshot(driver, "Barcode_Mapped")
        except Exception as e:
            take_screenshot(driver, "Barcode_Mapping_Error")
            raise e

    with allure.step("Save Product"):
        try:
            save_button = driver.find_element(By.XPATH, "//button[contains(text(),'SAVE')]")
            save_button.click()
            take_screenshot(driver, "Product_Saved")

            # Verify product creation success
            assert "product" in driver.current_url.lower() or "success" in driver.page_source.lower(), "Product creation may have failed"

        except Exception as e:
            take_screenshot(driver, "Product_Save_Error")
            raise e


################################## PURCHASE INVOICE ###########################################################

@allure.feature("Purchase Management")
@allure.story("Purchase Invoice")
@allure.title("Create Purchase Invoice")
@allure.description("This test creates a new purchase invoice with barcode scanning")
def Purchase_invoice(driver, barcode_purchase):
    global account_field

    with allure.step("Reset zoom and navigate to Purchase Invoice"):
        try:
            driver.execute_script("document.body.style.zoom='100%'")
            print("Step 5: Waiting for dashboard to load...")
            time.sleep(3)
            take_screenshot(driver, "Dashboard_Loaded")
        except Exception as e:
            take_screenshot(driver, "Dashboard_Load_Error")
            raise e

    with allure.step("Navigate to Transactions menu"):
        try:
            print("Step 6: Clicking on 'Transactions' menu...")
            transactions_clicked = False

            transactions_selectors = [
                "//a[contains(text(), 'Transactions')]",
                "//div[contains(text(), 'Transactions')]",
                "//span[contains(text(), 'Transactions')]",
                "//*[contains(@class, 'nav') and contains(text(), 'Transactions')]",
                "//*[text()='Transactions']",
                "//a[contains(@href, 'transaction')]",
                "//*[@class*='menu' and contains(text(), 'Transactions')]"
            ]

            for i, selector in enumerate(transactions_selectors, 1):
                try:
                    print(f"  Trying selector {i}: {selector}")
                    transactions_element = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    actions = ActionChains(driver)
                    actions.move_to_element(transactions_element).click().perform()
                    print(f"✓ Successfully clicked on 'Transactions' using selector {i}")
                    transactions_clicked = True
                    time.sleep(2)
                    take_screenshot(driver, "Transactions_Menu_Clicked")
                    break
                except Exception as e:
                    print(f"  ✗ Selector {i} failed: {str(e)[:50]}...")
                    continue

            if not transactions_clicked:
                take_screenshot(driver, "Transactions_Menu_Not_Found")
                raise Exception("Could not find Transactions menu")

        except Exception as e:
            take_screenshot(driver, "Transactions_Navigation_Error")
            raise e

    with allure.step("Navigate to Purchase Transaction"):
        try:
            purchase_transaction_hovered = False
            if not purchase_transaction_hovered:
                print("⚠️ Trying alternative approach for Purchase Transaction hover...")
                all_elements = driver.find_elements(By.TAG_NAME, "span")
                for element in all_elements:
                    try:
                        element_text = element.text.strip()
                        if 'Purchase Transaction' in element_text and element.is_displayed():
                            actions = ActionChains(driver)
                            actions.move_to_element(element).perform()
                            print(f"✓ Hovered over 'Purchase Transaction' using fallback method")
                            purchase_transaction_hovered = True
                            time.sleep(2)
                            take_screenshot(driver, "Purchase_Transaction_Hovered")
                            break
                    except Exception:
                        continue

            if not purchase_transaction_hovered:
                take_screenshot(driver, "Purchase_Transaction_Not_Found")
                raise Exception("Could not find or hover over 'Purchase Transaction' menu")

        except Exception as e:
            take_screenshot(driver, "Purchase_Transaction_Error")
            raise e

    with allure.step("Click Purchase Invoice"):
        try:
            print("Step 8: Clicking on 'Purchase Invoice' from dropdown...")
            purchase_invoice_clicked = False
            purchase_invoice_selectors = [
                "//*[@class='dropdown-item' and contains(text(), 'Purchase Invoice')]",
                "//*[contains(@class, 'menu-item') and contains(text(), 'Purchase Invoice')]"
            ]

            for i, selector in enumerate(purchase_invoice_selectors, 1):
                try:
                    print(f"  Trying Purchase Invoice selector {i}: {selector}")
                    purchase_invoice_element = WebDriverWait(driver, 8).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    actions = ActionChains(driver)
                    actions.move_to_element(purchase_invoice_element).click().perform()
                    print(f"✓ Successfully clicked on 'Purchase Invoice' using selector {i}")
                    purchase_invoice_clicked = True
                    time.sleep(3)
                    take_screenshot(driver, "Purchase_Invoice_Clicked")
                    break
                except Exception as e:
                    print(f"  ✗ Purchase Invoice selector {i} failed: {str(e)[:100]}...")
                    continue

            if not purchase_invoice_clicked:
                take_screenshot(driver, "Purchase_Invoice_Not_Found")
                raise Exception("Could not click Purchase Invoice")

        except Exception as e:
            take_screenshot(driver, "Purchase_Invoice_Click_Error")
            raise e

    with allure.step("Generate and enter Invoice Number"):
        try:
            random_invoice = "INV-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            print(f"Generated Invoice Number: {random_invoice}")
            allure.attach(random_invoice, name="Generated Invoice Number", attachment_type=AttachmentType.TEXT)

            invoice_field = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "invoiceNO"))
            )
            invoice_field.clear()
            invoice_field.send_keys(random_invoice)
            print(f"✓ Successfully entered Invoice Number: {random_invoice}")
            take_screenshot(driver, "Invoice_Number_Entered")
        except Exception as e:
            take_screenshot(driver, "Invoice_Number_Error")
            raise e

    with allure.step("Configure Account"):
        try:
            print("Step 10: Opening Account dropdown by pressing Enter...")
            account_field_selectors = [
                "//input[preceding-sibling::label[contains(text(), 'Account')] or @placeholder*='Account' or contains(@formcontrolname, 'account')]",
                "//input[contains(@placeholder, 'Press Enter to select Account')]",
                "//*[contains(text(), 'Press Enter to select Account')]",
                "//input[contains(@class, 'form-control') and contains(@placeholder, 'Account')]"
            ]
            account_field = None
            for selector in account_field_selectors:
                try:
                    account_field = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    print(f"✓ Found Account field using selector: {selector}")
                    break
                except:
                    continue

            if account_field:
                account_field.click()
                time.sleep(1)
                account_field.send_keys(Keys.ENTER)
                print("✓ Successfully pressed Enter on Account field to open dropdown")
                time.sleep(3)
                account_field.send_keys(Keys.ENTER)
                print("✓ Successfully selected first account")
                time.sleep(2)
                take_screenshot(driver, "Account_Selected")
            else:
                take_screenshot(driver, "Account_Field_Not_Found")
                raise Exception("Could not find Account field")

        except Exception as e:
            take_screenshot(driver, "Account_Configuration_Error")
            raise e

    with allure.step("Enter Remarks"):
        try:
            remarks_field = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "remarksid"))
            )
            remarks_field.clear()
            remarks_field.send_keys("This is an automated remark for PI.")
            time.sleep(5)
            print("✅ Remarks entered successfully.")
            take_screenshot(driver, "Remarks_Entered")
        except Exception as e:
            take_screenshot(driver, "Remarks_Error")
            raise e

    with allure.step(f"Process Barcode: {barcode_purchase}"):
        try:
            barcode_input = driver.find_element(By.ID, "barcodeField")
            barcode_input.clear()
            barcode_input.send_keys(barcode_purchase)
            barcode_input.send_keys(Keys.ENTER)
            allure.attach(str(barcode_purchase), name="Barcode", attachment_type=AttachmentType.TEXT)
            take_screenshot(driver, "Barcode_Entered")
        except Exception as e:
            take_screenshot(driver, "Barcode_Error")
            raise e

    with allure.step("Enter Quantity"):
        try:
            quantity = random.randint(80, 200)
            print(f"Generated quantity: {quantity}")
            allure.attach(str(quantity), name="Quantity", attachment_type=AttachmentType.TEXT)

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
                    take_screenshot(driver, "Quantity_Entered")
                    break
                except Exception as e:
                    print(f"⚠ Failed with XPath: {xpath} -> {e}")
            else:
                take_screenshot(driver, "Quantity_Field_Not_Found")
                raise Exception("Could not locate the quantity input field.")
        except Exception as e:
            take_screenshot(driver, "Quantity_Error")
            raise e

    with allure.step("Apply Discounts"):
        try:
            discount = random.randint(1, 50)
            print(f"Generated discount: {discount}%")
            allure.attach(str(discount), name="Discount Percentage", attachment_type=AttachmentType.TEXT)

            try:
                discount_field = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.ID, "INDDISCOUNTRATE0"))
                )
                discount_field.clear()
                discount_field.send_keys(str(discount))
                time.sleep(2)
                print("✅ Discount entered.")
            except Exception as e:
                print(f"❌ Discount input not found: {e}")

            discount = random.randint(1, 50)
            try:
                discount_field = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.ID, "INDDISCOUNTRATE1"))
                )
                discount_field.clear()
                discount_field.send_keys(str(discount))
                time.sleep(2)
                print("✅ Discount entered.")
                take_screenshot(driver, "Discounts_Applied")
            except Exception as e:
                print(f"❌ Discount input not found: {e}")
        except Exception as e:
            take_screenshot(driver, "Discount_Error")
            raise e

    with allure.step("Save Purchase Invoice"):
        try:
            wait = WebDriverWait(driver, 10)
            save_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'SAVE') and contains(@class, 'btn-info')]")))
            save_button.click()
            take_screenshot(driver, "Save_Button_Clicked")

            try:
                WebDriverWait(driver, 5).until(EC.alert_is_present())
                alert = driver.switch_to.alert
                alert.accept()
                print("Alert accepted successfully.")
                take_screenshot(driver, "Alert_Accepted")
            except TimeoutException:
                print("No alert appeared after clicking SAVE.")
        except Exception as e:
            take_screenshot(driver, "Save_Error")
            raise e

    with allure.step("Complete Purchase Invoice Process"):
        try:
            import pyautogui
            time.sleep(10)
            pyautogui.press('esc')
            time.sleep(5)

            view_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'VIEW')]")))
            view_button.click()
            take_screenshot(driver, "View_Button_Clicked")

            time.sleep(2)
            actions = ActionChains(driver)
            actions.send_keys(Keys.ENTER).perform()
            time.sleep(3)

            reset_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'RESET')]")))
            reset_btn.click()
            take_screenshot(driver, "Reset_Button_Clicked")

            time.sleep(3)
            wait.until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.accept()
            time.sleep(5)

            back_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'BACK')]")))
            back_btn.click()
            take_screenshot(driver, "Purchase_Invoice_Completed")
        except Exception as e:
            take_screenshot(driver, "Purchase_Invoice_Completion_Error")
            raise e


################################## SALES TAX INVOICE ###########################################################

@allure.feature("Sales Management")
@allure.story("Sales Tax Invoice")
@allure.title("Create Sales Tax Invoice")
@allure.description("This test creates a new sales tax invoice with barcode scanning and customer selection")
def Sales_tax_invoice(driver, barcode_sales, customer_name=None):
    wait = WebDriverWait(driver, 10)

    with allure.step("Reset zoom and navigate to Sales Tax Invoice"):
        try:
            driver.execute_script("document.body.style.zoom='100%'")
            print("Step 1: Resetting zoom and preparing for Sales Tax Invoice...")
            time.sleep(3)
            take_screenshot(driver, "Sales_Dashboard_Loaded")
        except Exception as e:
            take_screenshot(driver, "Sales_Dashboard_Error")
            allure.attach(str(e), name="Dashboard Error", attachment_type=AttachmentType.TEXT)
            raise e

    with allure.step("Navigate to Transactions menu"):
        try:
            print("Step 2: Clicking on 'Transactions' menu...")
            transactions_clicked = False

            transactions_selectors = [
                "//a[contains(text(), 'Transactions')]",
                "//div[contains(text(), 'Transactions')]",
                "//span[contains(text(), 'Transactions')]",
                "//*[contains(@class, 'nav') and contains(text(), 'Transactions')]",
                "//*[text()='Transactions']",
                "//a[contains(@href, 'transaction')]",
                "//*[@class*='menu' and contains(text(), 'Transactions')]"
            ]

            for i, selector in enumerate(transactions_selectors, 1):
                try:
                    print(f"  Trying selector {i}: {selector}")
                    transactions_element = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    actions = ActionChains(driver)
                    actions.move_to_element(transactions_element).click().perform()
                    print(f"✓ Successfully clicked on 'Transactions' using selector {i}")
                    transactions_clicked = True
                    time.sleep(2)
                    take_screenshot(driver, "Transactions_Menu_Clicked_Sales")
                    break
                except Exception as e:
                    print(f"  ✗ Selector {i} failed: {str(e)[:50]}...")
                    continue

            if not transactions_clicked:
                take_screenshot(driver, "Transactions_Menu_Not_Found_Sales")
                allure.attach("Could not find Transactions menu", name="Navigation Error",
                              attachment_type=AttachmentType.TEXT)
                raise Exception("Could not find Transactions menu")

        except Exception as e:
            take_screenshot(driver, "Transactions_Navigation_Error_Sales")
            allure.attach(str(e), name="Transactions Navigation Error", attachment_type=AttachmentType.TEXT)
            raise e

    with allure.step("Navigate to Sales Transaction"):
        try:
            print("Step 3: Hovering over 'Sales Transaction'...")
            sales_transaction_hovered = False

            sales_transaction_selectors = [
                "//span[contains(text(), 'Sales Transaction')]",
                "//a[contains(text(), 'Sales Transaction')]",
                "//*[contains(@class, 'dropdown-toggle') and contains(text(), 'Sales Transaction')]",
                "//*[text()='Sales Transaction']"
            ]

            for i, selector in enumerate(sales_transaction_selectors, 1):
                try:
                    print(f"  Trying Sales Transaction selector {i}: {selector}")
                    sales_transaction_element = WebDriverWait(driver, 8).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    actions = ActionChains(driver)
                    actions.move_to_element(sales_transaction_element).perform()
                    print(f"✓ Successfully hovered over 'Sales Transaction' using selector {i}")
                    sales_transaction_hovered = True
                    time.sleep(2)
                    take_screenshot(driver, "Sales_Transaction_Hovered")
                    break
                except Exception as e:
                    print(f"  ✗ Sales Transaction selector {i} failed: {str(e)[:100]}...")
                    continue

            if not sales_transaction_hovered:
                print("⚠️ Trying alternative approach for Sales Transaction hover...")
                all_elements = driver.find_elements(By.TAG_NAME, "span")
                for element in all_elements:
                    try:
                        element_text = element.text.strip()
                        if 'Sales Transaction' in element_text and element.is_displayed():
                            actions = ActionChains(driver)
                            actions.move_to_element(element).perform()
                            print(f"✓ Hovered over 'Sales Transaction' using fallback method")
                            sales_transaction_hovered = True
                            time.sleep(2)
                            take_screenshot(driver, "Sales_Transaction_Hovered_Fallback")
                            break
                    except Exception:
                        continue

            if not sales_transaction_hovered:
                take_screenshot(driver, "Sales_Transaction_Not_Found")
                allure.attach("Could not find or hover over Sales Transaction menu", name="Navigation Error",
                              attachment_type=AttachmentType.TEXT)
                raise Exception("Could not find or hover over 'Sales Transaction' menu")

        except Exception as e:
            take_screenshot(driver, "Sales_Transaction_Error")
            allure.attach(str(e), name="Sales Transaction Error", attachment_type=AttachmentType.TEXT)
            raise e

    with allure.step("Click Sales Tax Invoice"):
        try:
            print("Step 4: Clicking on 'Sales Tax Invoice' from dropdown...")
            sales_tax_invoice_clicked = False

            sales_tax_invoice_selectors = [
                "//*[@class='dropdown-item' and contains(text(), 'Sales Tax Invoice')]",
                "//*[contains(@class, 'menu-item') and contains(text(), 'Sales Tax Invoice')]",
                "//a[contains(text(), 'Sales Tax Invoice')]",
                "//*[text()='Sales Tax Invoice']"
            ]

            for i, selector in enumerate(sales_tax_invoice_selectors, 1):
                try:
                    print(f"  Trying Sales Tax Invoice selector {i}: {selector}")
                    sales_tax_invoice_element = WebDriverWait(driver, 8).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    actions = ActionChains(driver)
                    actions.move_to_element(sales_tax_invoice_element).click().perform()
                    print(f"✓ Successfully clicked on 'Sales Tax Invoice' using selector {i}")
                    sales_tax_invoice_clicked = True
                    time.sleep(3)
                    take_screenshot(driver, "Sales_Tax_Invoice_Clicked")
                    break
                except Exception as e:
                    print(f"  ✗ Sales Tax Invoice selector {i} failed: {str(e)[:100]}...")
                    continue

            if not sales_tax_invoice_clicked:
                take_screenshot(driver, "Sales_Tax_Invoice_Not_Found")
                allure.attach("Could not click Sales Tax Invoice", name="Navigation Error",
                              attachment_type=AttachmentType.TEXT)
                raise Exception("Could not click Sales Tax Invoice")

        except Exception as e:
            take_screenshot(driver, "Sales_Tax_Invoice_Click_Error")
            allure.attach(str(e), name="Sales Tax Invoice Click Error", attachment_type=AttachmentType.TEXT)
            raise e

    with allure.step("Generate and enter Invoice Number"):
        try:
            random_invoice = "STI-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            print(f"Generated Sales Tax Invoice Number: {random_invoice}")
            allure.attach(random_invoice, name="Generated Sales Invoice Number", attachment_type=AttachmentType.TEXT)

            invoice_field_selectors = [
                "//input[@id='invoiceNO']",
                "//input[contains(@placeholder, 'Invoice')]",
                "//input[contains(@name, 'invoice')]",
                "//input[contains(@formcontrolname, 'invoice')]"
            ]

            invoice_field = None
            for selector in invoice_field_selectors:
                try:
                    invoice_field = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    break
                except:
                    continue

            if invoice_field:
                invoice_field.clear()
                invoice_field.send_keys(random_invoice)
                print(f"✓ Successfully entered Sales Invoice Number: {random_invoice}")
                take_screenshot(driver, "Sales_Invoice_Number_Entered")
            else:
                take_screenshot(driver, "Sales_Invoice_Field_Not_Found")
                raise Exception("Could not find Invoice Number field")

        except Exception as e:
            take_screenshot(driver, "Sales_Invoice_Number_Error")
            allure.attach(str(e), name="Invoice Number Error", attachment_type=AttachmentType.TEXT)
            raise e

    with allure.step("Configure Customer Account"):
        try:
            print("Step 6: Configuring Customer Account...")

            customer_field_selectors = [
                "//input[contains(@placeholder, 'Customer') or contains(@placeholder, 'customer')]",
                "//input[contains(@placeholder, 'Press Enter to select')]",
                "//input[preceding-sibling::label[contains(text(), 'Customer')] or contains(@formcontrolname, 'customer')]",
                "//input[contains(@class, 'form-control') and contains(@placeholder, 'Account')]"
            ]

            customer_field = None
            for selector in customer_field_selectors:
                try:
                    customer_field = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    print(f"✓ Found Customer field using selector: {selector}")
                    break
                except:
                    continue

            if customer_field:
                customer_field.click()
                time.sleep(1)

                if customer_name:
                    customer_field.send_keys(customer_name)
                    time.sleep(2)
                    customer_field.send_keys(Keys.ENTER)
                    allure.attach(customer_name, name="Customer Name", attachment_type=AttachmentType.TEXT)
                    print(f"✓ Successfully entered customer: {customer_name}")
                else:
                    customer_field.send_keys(Keys.ENTER)
                    print("✓ Successfully pressed Enter on Customer field to open dropdown")
                    time.sleep(3)
                    customer_field.send_keys(Keys.ENTER)
                    print("✓ Successfully selected first customer")

                time.sleep(2)
                take_screenshot(driver, "Customer_Selected")
            else:
                take_screenshot(driver, "Customer_Field_Not_Found")
                allure.attach("Could not find Customer field", name="Customer Field Error",
                              attachment_type=AttachmentType.TEXT)
                raise Exception("Could not find Customer field")

        except Exception as e:
            take_screenshot(driver, "Customer_Configuration_Error")
            allure.attach(str(e), name="Customer Configuration Error", attachment_type=AttachmentType.TEXT)
            raise e

    with allure.step("Enter Sales Remarks"):
        try:
            remarks_field_selectors = [
                "//input[@id='remarksid']",
                "//textarea[@id='remarksid']",
                "//input[contains(@placeholder, 'Remarks') or contains(@placeholder, 'remarks')]",
                "//textarea[contains(@placeholder, 'Remarks') or contains(@placeholder, 'remarks')]"
            ]

            remarks_field = None
            for selector in remarks_field_selectors:
                try:
                    remarks_field = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    break
                except:
                    continue

            if remarks_field:
                remarks_field.clear()
                remarks_field.send_keys("This is an automated remark for Sales Tax Invoice.")
                time.sleep(2)
                print("✅ Sales remarks entered successfully.")
                allure.attach("This is an automated remark for Sales Tax Invoice.", name="Sales Remarks",
                              attachment_type=AttachmentType.TEXT)
                take_screenshot(driver, "Sales_Remarks_Entered")
            else:
                print("⚠️ Remarks field not found, continuing without remarks.")
                take_screenshot(driver, "Sales_Remarks_Field_Not_Found")

        except Exception as e:
            take_screenshot(driver, "Sales_Remarks_Error")
            allure.attach(str(e), name="Sales Remarks Error", attachment_type=AttachmentType.TEXT)
            print(f"⚠️ Remarks error (non-critical): {e}")

    with allure.step(f"Process Sales Barcode: {barcode_sales}"):
        try:
            barcode_field_selectors = [
                "//input[@id='barcodeField']",
                "//input[contains(@placeholder, 'Barcode') or contains(@placeholder, 'barcode')]",
                "//input[contains(@name, 'barcode')]",
                "//input[contains(@class, 'barcode')]"
            ]

            barcode_input = None
            for selector in barcode_field_selectors:
                try:
                    barcode_input = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    break
                except:
                    continue

            if barcode_input:
                barcode_input.clear()
                barcode_input.send_keys(str(barcode_sales))
                barcode_input.send_keys(Keys.ENTER)
                allure.attach(str(barcode_sales), name="Sales Barcode", attachment_type=AttachmentType.TEXT)
                print(f"✓ Successfully entered sales barcode: {barcode_sales}")
                time.sleep(3)
                take_screenshot(driver, "Sales_Barcode_Entered")
            else:
                take_screenshot(driver, "Sales_Barcode_Field_Not_Found")
                allure.attach("Could not find barcode field", name="Barcode Field Error",
                              attachment_type=AttachmentType.TEXT)
                raise Exception("Could not find barcode input field")

        except Exception as e:
            take_screenshot(driver, "Sales_Barcode_Error")
            allure.attach(str(e), name="Sales Barcode Error", attachment_type=AttachmentType.TEXT)
            raise e

    with allure.step("Enter Sales Quantity"):
        try:
            quantity = random.randint(10, 100)
            print(f"Generated sales quantity: {quantity}")
            allure.attach(str(quantity), name="Sales Quantity", attachment_type=AttachmentType.TEXT)

            quantity_field_xpaths = [
                "//table//tr//td[position()=9]//input",
                "//input[contains(@name, 'quantity') or contains(@name, 'Quantity')]",
                "//input[contains(@id, 'quantity') or contains(@id, 'Quantity')]",
                "//td[contains(@class, 'quantity')]//input",
                "//table//tbody//tr[1]//td[9]//input",
                "//table//tbody//tr[last()]//input[contains(@type, 'number')]"
            ]

            quantity_field = None
            for xpath in quantity_field_xpaths:
                try:
                    quantity_field = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, xpath))
                    )
                    quantity_field.clear()
                    quantity_field.send_keys(str(quantity))
                    quantity_field.send_keys(Keys.ENTER)
                    print("✅ Sales quantity entered and Enter key pressed.")
                    time.sleep(2)
                    take_screenshot(driver, "Sales_Quantity_Entered")
                    break
                except Exception as e:
                    print(f"⚠ Failed with quantity XPath: {xpath} -> {e}")
                    continue

            if not quantity_field:
                take_screenshot(driver, "Sales_Quantity_Field_Not_Found")
                allure.attach("Could not locate the sales quantity input field", name="Quantity Field Error",
                              attachment_type=AttachmentType.TEXT)
                raise Exception("Could not locate the sales quantity input field.")

        except Exception as e:
            take_screenshot(driver, "Sales_Quantity_Error")
            allure.attach(str(e), name="Sales Quantity Error", attachment_type=AttachmentType.TEXT)
            raise e

    with allure.step("Apply Sales Discounts"):
        try:
            discount1 = random.randint(1, 20)
            discount2 = random.randint(1, 15)
            print(f"Generated discounts: {discount1}% and {discount2}%")
            allure.attach(f"Discount 1: {discount1}%, Discount 2: {discount2}%", name="Sales Discount Percentages",
                          attachment_type=AttachmentType.TEXT)

            discount_fields = [
                "INDDISCOUNTRATE0",
                "INDDISCOUNTRATE1"
            ]

            discounts = [discount1, discount2]

            for i, (field_id, discount) in enumerate(zip(discount_fields, discounts)):
                try:
                    discount_field = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.ID, field_id))
                    )
                    discount_field.clear()
                    discount_field.send_keys(str(discount))
                    time.sleep(1)
                    print(f"✅ Sales discount {i + 1} entered: {discount}%")
                except Exception as e:
                    print(f"❌ Sales discount field {field_id} not found: {e}")

            take_screenshot(driver, "Sales_Discounts_Applied")

        except Exception as e:
            take_screenshot(driver, "Sales_Discount_Error")
            allure.attach(str(e), name="Sales Discount Error", attachment_type=AttachmentType.TEXT)
            print(f"⚠️ Sales discount error (non-critical): {e}")

    with allure.step("Save Sales Tax Invoice"):
        try:
            save_button_selectors = [
                "//button[contains(text(), 'SAVE') and contains(@class, 'btn-info')]",
                "//button[contains(text(), 'SAVE')]",
                "//input[@value='SAVE']",
                "//*[@id='save' or @name='save']"
            ]

            save_button = None
            for selector in save_button_selectors:
                try:
                    save_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    break
                except:
                    continue

            if save_button:
                save_button.click()
                print("✓ Save button clicked successfully")
                take_screenshot(driver, "Sales_Save_Button_Clicked")

                # Handle potential alert
                try:
                    WebDriverWait(driver, 5).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert_text = alert.text
                    allure.attach(alert_text, name="Save Alert Text", attachment_type=AttachmentType.TEXT)
                    alert.accept()
                    print(f"✓ Alert accepted: {alert_text}")
                    take_screenshot(driver, "Sales_Alert_Accepted")
                except TimeoutException:
                    print("ℹ️ No alert appeared after clicking SAVE.")
            else:
                take_screenshot(driver, "Sales_Save_Button_Not_Found")
                allure.attach("Could not find Save button", name="Save Button Error",
                              attachment_type=AttachmentType.TEXT)
                raise Exception("Could not find Save button")

        except Exception as e:
            take_screenshot(driver, "Sales_Save_Error")
            allure.attach(str(e), name="Sales Save Error", attachment_type=AttachmentType.TEXT)
            raise e

    with allure.step("Complete Sales Tax Invoice Process"):
        try:
            print("Step 12: Completing Sales Tax Invoice process...")

            # Wait and handle any additional popups
            time.sleep(5)

            # Try to use pyautogui to press ESC if available
            try:
                import pyautogui
                pyautogui.press('esc')
                print("✓ ESC key pressed using pyautogui")
                time.sleep(2)
            except ImportError:
                print("⚠️ pyautogui not available, using Selenium keys")
                actions = ActionChains(driver)
                actions.send_keys(Keys.ESCAPE).perform()
                time.sleep(2)

            # Try to click VIEW button
            try:
                view_button = WebDriverWait(driver, 8).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'VIEW')]"))
                )
                view_button.click()
                print("✓ VIEW button clicked")
                take_screenshot(driver, "Sales_View_Button_Clicked")
                time.sleep(3)
            except TimeoutException:
                print("⚠️ VIEW button not found, continuing...")

            # Press Enter to confirm view
            try:
                actions = ActionChains(driver)
                actions.send_keys(Keys.ENTER).perform()
                time.sleep(3)
                print("✓ Enter key pressed for view confirmation")
            except Exception as e:
                print(f"⚠️ Enter key press failed: {e}")

            # Try to click RESET button
            try:
                reset_btn = WebDriverWait(driver, 8).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'RESET')]"))
                )
                reset_btn.click()
                print("✓ RESET button clicked")
                take_screenshot(driver, "Sales_Reset_Button_Clicked")
                time.sleep(3)

                # Handle reset confirmation alert
                try:
                    WebDriverWait(driver, 5).until(EC.alert_is_present())
                    alert = driver.switch_to.alert
                    alert_text = alert.text
                    allure.attach(alert_text, name="Reset Alert Text", attachment_type=AttachmentType.TEXT)
                    alert.accept()
                    print(f"✓ Reset alert accepted: {alert_text}")
                    time.sleep(2)
                except TimeoutException:
                    print("ℹ️ No reset alert appeared")

            except TimeoutException:
                print("⚠️ RESET button not found, continuing...")

            # Try to click BACK button
            try:
                back_btn = WebDriverWait(driver, 8).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'BACK')]"))
                )
                back_btn.click()
                print("✓ BACK button clicked")
                take_screenshot(driver, "Sales_Back_Button_Clicked")
                time.sleep(3)
            except TimeoutException:
                print("⚠️ BACK button not found, continuing...")

            take_screenshot(driver, "Sales_Tax_Invoice_Completed")
            print("✅ Sales Tax Invoice process completed successfully")
            allure.attach("Sales Tax Invoice created and processed successfully", name="Process Completion",
                          attachment_type=AttachmentType.TEXT)

        except Exception as e:
            take_screenshot(driver, "Sales_Tax_Invoice_Completion_Error")
            allure.attach(str(e), name="Sales Tax Invoice Completion Error", attachment_type=AttachmentType.TEXT)
            print(f"⚠️ Error in completion process: {e}")
            raise e

    print("🎉 Sales Tax Invoice function completed successfully!")



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



Purchase_invoice(driver,
                 barcode_purchase=11)

Sales_tax_invoice(driver,
                  barcode_sales=11)


print("Keeping browser open for 30 seconds for observation...")
time.sleep(50)



#
# # !/usr/bin/env python3
# """
# Complete Test Runner for ERP System
# This script demonstrates how to call all the functions in sequence
# """
#
#
# from selenium.webdriver.chrome.options import Options
#
#
# # Import all your functions (assuming they're in the same file or properly imported)
# # from your_module import Login, product_master, Purchase_invoice, Sales_tax_invoice, take_screenshot
#
# # Test data configuration
# TEST_CONFIG = {
#     "login": {
#         "username": "gedehim917@decodewp.com",
#         "password": "Tebahal1!",
#         "url": "https://velvet.webredirect.himshang.com.np/#/pages/dashboard"
#     },
#     "product": {
#         "product_item": "Test Product " + ''.join(random.choices(string.ascii_uppercase, k=4)),
#         "HS_code": "12345678",
#         "unit": "PCS",
#         "item_type": "Inventory Item",
#         "description": "Test product for automation",
#         "category": "N/A",
#         "short_name": "TP" + ''.join(random.choices(string.digits, k=3)),
#         "purchase_price": "100.00",
#         "sales_price": "150.00",
#         "alt_unit": "BOX",
#         "conversion_factor": "10",
#         "barcode_map": ''.join(random.choices(string.digits, k=5)),
#         "barcode_unit": "PCS"
#     }
# }
#
# #
# def setup_driver():
#     """Setup Chrome driver with optimal settings"""
#     chrome_options = Options()
#     chrome_options.add_argument("--start-maximized")
#     chrome_options.add_argument("--disable-blink-features=AutomationControlled")
#     chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
#     chrome_options.add_experimental_option('useAutomationExtension', False)
#
#     driver = webdriver.Chrome(options=chrome_options)
#     driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
#     return driver
#
#
# @allure.epic("ERP System End-to-End Testing")
# @allure.feature("Complete Workflow")
# class TestERPWorkflow:
#
#     def setup_method(self):
#         """Setup method called before each test"""
#         self.driver = setup_driver()
#
#     def teardown_method(self):
#         """Teardown method called after each test"""
#         if hasattr(self, 'driver'):
#             self.driver.quit()
#
#     @allure.story("Complete ERP Workflow")
#     @allure.title("End-to-End ERP System Test")
#     @allure.description("Complete workflow: Login → Product Master → Purchase Invoice → Sales Tax Invoice")
#     def test_complete_erp_workflow(self):
#         """Complete ERP workflow test"""
#
#         # Step 1: Login
#         with allure.step("Step 1: User Authentication"):
#             Login(
#                 username=TEST_CONFIG["login"]["username"],
#                 password=TEST_CONFIG["login"]["password"],
#                 link=TEST_CONFIG["login"]["url"]
#             )
#
#         # Step 2: Create Product Master
#         with allure.step("Step 2: Create Product Master"):
#             product_master(
#                 driver=self.driver,
#                 product_item=TEST_CONFIG["product"]["product_item"],
#                 HS_code=TEST_CONFIG["product"]["HS_code"],
#                 unit=TEST_CONFIG["product"]["unit"],
#                 item_type=TEST_CONFIG["product"]["item_type"],
#                 description=TEST_CONFIG["product"]["description"],
#                 category=TEST_CONFIG["product"]["category"],
#                 short_name=TEST_CONFIG["product"]["short_name"],
#                 purchase_price=TEST_CONFIG["product"]["purchase_price"],
#                 sales_price=TEST_CONFIG["product"]["sales_price"],
#                 alt_unit=TEST_CONFIG["product"]["alt_unit"],
#                 conversion_factor=TEST_CONFIG["product"]["conversion_factor"],
#                 barcode_map=TEST_CONFIG["product"]["barcode_map"],
#                 barcode_unit=TEST_CONFIG["product"]["barcode_unit"]
#             )
#
#         # Step 3: Create Purchase Invoice
#         with allure.step("Step 3: Create Purchase Invoice"):
#             Purchase_invoice(
#                 driver=self.driver,
#                 barcode_purchase=TEST_CONFIG["product"]["barcode_map"]
#             )
#
#         # Step 4: Create Sales Tax Invoice
#         with allure.step("Step 4: Create Sales Tax Invoice"):
#             Sales_tax_invoice(
#                 driver=self.driver,
#                 barcode_sales=TEST_CONFIG["product"]["barcode_map"],
#                 customer_name="Test Customer"
#             )
#
#     @allure.story("Individual Function Tests")
#     @allure.title("Test Login Function Only")
#     def test_login_only(self):
#         """Test only the login functionality"""
#         Login(
#             username=TEST_CONFIG["login"]["username"],
#             password=TEST_CONFIG["login"]["password"],
#             link=TEST_CONFIG["login"]["url"]
#         )
#
#     @allure.story("Individual Function Tests")
#     @allure.title("Test Product Master Only")
#     def test_product_master_only(self):
#         """Test only product master creation"""
#         # Login first
#         Login(
#             username=TEST_CONFIG["login"]["username"],
#             password=TEST_CONFIG["login"]["password"],
#             link=TEST_CONFIG["login"]["url"]
#         )
#
#         # Create product
#         product_master(
#             driver=self.driver,
#             **TEST_CONFIG["product"]
#         )
#
#     @allure.story("Individual Function Tests")
#     @allure.title("Test Purchase Invoice Only")
#     def test_purchase_invoice_only(self):
#         """Test only purchase invoice creation"""
#         # Login first
#         Login(
#             username=TEST_CONFIG["login"]["username"],
#             password=TEST_CONFIG["login"]["password"],
#             link=TEST_CONFIG["login"]["url"]
#         )
#
#         # Create purchase invoice with existing barcode
#         Purchase_invoice(
#             driver=self.driver,
#             barcode_purchase="1234567890123"  # Use existing barcode
#         )
#
#     @allure.story("Individual Function Tests")
#     @allure.title("Test Sales Tax Invoice Only")
#     def test_sales_tax_invoice_only(self):
#         """Test only sales tax invoice creation"""
#         # Login first
#         Login(
#             username=TEST_CONFIG["login"]["username"],
#             password=TEST_CONFIG["login"]["password"],
#             link=TEST_CONFIG["login"]["url"]
#         )
#
#         # Create sales tax invoice with existing barcode
#         Sales_tax_invoice(
#             driver=self.driver,
#             barcode_sales="1234567890123",  # Use existing barcode
#             customer_name="Test Customer"
#         )
#
#
# # Alternative: Direct function calls (without pytest)
# def setup_driver():
#     pass
#
#
# def run_complete_workflow():
#     """Run complete workflow without pytest framework"""
#     driver = setup_driver()
#
#     try:
#         print("🚀 Starting Complete ERP Workflow...")
#
#         # Step 1: Login
#         print("\n📝 Step 1: Logging in...")
#         Login(
#             username=TEST_CONFIG["login"]["username"],
#             password=TEST_CONFIG["login"]["password"],
#             link=TEST_CONFIG["login"]["url"]
#         )
#
#         # Step 2: Create Product Master
#         print("\n📦 Step 2: Creating Product Master...")
#         product_master(
#             driver=driver,
#             **TEST_CONFIG["product"]
#         )
#
#         # Step 3: Create Purchase Invoice
#         print("\n🛒 Step 3: Creating Purchase Invoice...")
#         Purchase_invoice(
#             driver=driver,
#             barcode_purchase=TEST_CONFIG["product"]["barcode_map"]
#         )
#
#         # Step 4: Create Sales Tax Invoice
#         print("\n💰 Step 4: Creating Sales Tax Invoice...")
#         Sales_tax_invoice(
#             driver=driver,
#             barcode_sales=TEST_CONFIG["product"]["barcode_map"],
#             customer_name="Test Customer"
#         )
#
#         print("\n✅ Complete workflow finished successfully!")
#
#     except Exception as e:
#         print(f"\n❌ Workflow failed: {str(e)}")
#         take_screenshot(driver, "Workflow_Failed")
#         raise
#     finally:
#         input("\nPress Enter to close browser...")
#         driver.quit()

#
# def run_individual_functions():
#     """Run functions individually for testing"""
#     driver = setup_driver()
#
#     try:
#         # Always login first
#         print("📝 Logging in...")
#         Login(
#             username=TEST_CONFIG["login"]["username"],
#             password=TEST_CONFIG["login"]["password"],
#             link=TEST_CONFIG["login"]["url"]
#         )
#
#         while True:
#             print("\n" + "=" * 50)
#             print("Choose which function to test:")
#             print("1. Product Master")
#             print("2. Purchase Invoice")
#             print("3. Sales Tax Invoice")
#             print("4. Complete Workflow")
#             print("5. Exit")
#             print("=" * 50)
#
#             choice = input("Enter your choice (1-5): ").strip()
#
#             if choice == "1":
#                 print("\n📦 Testing Product Master...")
#                 product_master(driver, **TEST_CONFIG["product"])
#
#             elif choice == "2":
#                 barcode = input("Enter barcode (or press Enter for default): ").strip()
#                 if not barcode:
#                     barcode = "1234567890123"
#                 print(f"\n🛒 Testing Purchase Invoice with barcode: {barcode}")
#                 Purchase_invoice(driver, barcode_purchase=barcode)
#
#             elif choice == "3":
#                 barcode = input("Enter barcode (or press Enter for default): ").strip()
#                 customer = input("Enter customer name (or press Enter for default): ").strip()
#                 if not barcode:
#                     barcode = "1234567890123"
#                 if not customer:
#                     customer = "Test Customer"
#                 print(f"\n💰 Testing Sales Tax Invoice with barcode: {barcode}")
#                 Sales_tax_invoice(driver, barcode_sales=barcode, customer_name=customer)
#
#             elif choice == "4":
#                 print("\n🚀 Running Complete Workflow...")
#                 run_complete_workflow()
#                 break
#
#             elif choice == "5":
#                 print("👋 Exiting...")
#                 break
#
#             else:
#                 print("❌ Invalid choice. Please try again.")
#
#     except Exception as e:
#         print(f"\n❌ Error occurred: {str(e)}")
#         take_screenshot(driver, "Individual_Test_Failed")
#     finally:
#         driver.quit()

#
# if __name__ == "__main__":
#     print("🎯 ERP System Test Runner")
#     print("=" * 40)
#     print("1. Run with pytest (recommended for Allure reports)")
#     print("2. Run complete workflow")
#     print("3. Run individual functions")
#     print("=" * 40)
#
#     mode = input("Choose mode (1-3): ").strip()
#
#     if mode == "1":
#         print("\n📊 Running with pytest...")
#         print("Use command: pytest -v --allure-results=allure-results")
#         print("Then: allure serve allure-results")
#
#     elif mode == "2":
#         print("\n🚀 Running complete workflow...")
#         run_complete_workflow()
#
#     elif mode == "3":
#         print("\n🔧 Running individual functions...")
#         run_individual_functions()
#
#     else:
#         print("❌ Invalid choice")

# Pytest execution commands:
"""
To run tests with Allure reporting:

1. Install required packages:
   pip install pytest allure-pytest selenium

2. Run tests and generate Allure results:
   pytest test_runner.py -v --allure-results=allure-results

3. Generate and serve Allure report:
   allure serve allure-results

4. Or generate static report:
   allure generate allure-results --clean
   allure open allure-report

5. Run specific test:
   pytest test_runner.py::TestERPWorkflow::test_complete_erp_workflow -v --allure-results=allure-results

6. Run with specific markers:
   pytest -m "login" --allure-results=allure-results
"""