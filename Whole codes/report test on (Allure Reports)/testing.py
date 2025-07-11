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

##########################################LOG IN###########################################################

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




########################################## PRODUCT MASTER ###########################################################



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




################################## PURCHASE INVOICE ###########################################################

def Purchase_invoice(driver, barcode_purchase):
    global account_field
    driver.execute_script("document.body.style.zoom='100%'")
    try:
        # ============ NAVIGATION TO PURCHASE TRANSACTION ============
        print("Step 5: Waiting for dashboard to load...")
        time.sleep(3)  # Give additional time for page to fully load

        print("Step 6: Clicking on 'Transactions' menu...")
        transactions_clicked = False

        print("Step 6.1: Debugging available navigation elements...")
        try:
            nav_elements = driver.find_elements(By.XPATH, "//a | //div[@class*='nav'] | //span[@class*='nav']")
            print(f"Found {len(nav_elements)} potential navigation elements")

            visible_nav_texts = []
            for element in nav_elements[:15]:
                try:
                    text = element.text.strip()
                    if text and len(text) > 0 and element.is_displayed():
                        visible_nav_texts.append(text)
                except:
                    pass

            print("Available navigation texts:")
            for text in visible_nav_texts:
                print(f"  - '{text}'")
        except Exception as e:
            print(f"Navigation debug failed: {e}")

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
                break
            except Exception as e:
                print(f"  ✗ Selector {i} failed: {str(e)[:50]}...")
                continue

        purchase_transaction_hovered = False
        if not purchase_transaction_hovered:
            print("⚠️ Trying alternative approach for Purchase Transaction hover...")
            try:
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
                            break
                    except Exception:
                        continue
            except Exception as e:
                print(f"⚠️ Fallback method for Purchase Transaction hover failed: {e}")

        if not purchase_transaction_hovered:
            raise Exception("Could not find or hover over 'Purchase Transaction' menu")

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
                break
            except Exception as e:
                print(f"  ✗ Purchase Invoice selector {i} failed: {str(e)[:100]}...")
                continue

        if not purchase_invoice_clicked:
            print("⚠️ Trying alternative approach for Purchase Invoice...")
            try:
                invoice_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Purchase Invoice')]")
                print(f"Found {len(invoice_elements)} elements containing 'Purchase Invoice'")
                for element in invoice_elements:
                    try:
                        if element.is_displayed() and element.is_enabled():
                            actions = ActionChains(driver)
                            actions.move_to_element(element).click().perform()
                            print(f"✓ Clicked on 'Purchase Invoice' using fallback method")
                            purchase_invoice_clicked = True
                            time.sleep(3)
                            break
                    except Exception:
                        continue
            except Exception as e:
                print(f"⚠️ Fallback method for Purchase Invoice failed: {e}")

        print("Step 9: Manually typing in Invoice Number field...")

        random_invoice = "INV-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        print(f"Generated Invoice Number: {random_invoice}")

        try:
            invoice_field = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "invoiceNO"))
            )
            invoice_field.clear()
            invoice_field.send_keys(random_invoice)
            print(f"✓ Successfully entered Invoice Number: {random_invoice}")
        except Exception as e:
            print(f"⚠️ Failed to enter Invoice Number: {e}")

        print("Step 10: Opening Account dropdown by pressing Enter...")
        try:
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
                print("⏳ Waiting for dropdown list to load completely...")
                time.sleep(3)
            else:
                raise Exception("Could not find Account field")

        except Exception as e:
            print(f"⚠️ Failed to open Account dropdown using primary method: {e}")
            try:
                all_inputs = driver.find_elements(By.TAG_NAME, "input")
                for input_field in all_inputs:
                    try:
                        placeholder = input_field.get_attribute("placeholder")
                        if placeholder and "account" in placeholder.lower():
                            input_field.click()
                            time.sleep(1)
                            input_field.send_keys(Keys.ENTER)
                            print("✓ Successfully opened Account dropdown using fallback method")
                            time.sleep(2)
                            break
                    except:
                        continue
            except Exception as e2:
                print(f"⚠️ All methods failed to open Account dropdown: {e2}")

        print("Step 11: Selecting first account by pressing Enter again...")
        try:
            if account_field:
                account_field.send_keys(Keys.ENTER)
                print("✓ Successfully pressed Enter again to select first account")
                time.sleep(2)
            else:
                focused_element = driver.switch_to.active_element
                focused_element.send_keys(Keys.ENTER)
                print("✓ Successfully pressed Enter on focused element to select first account")
                time.sleep(2)
        except Exception as e:
            print(f"⚠️ Failed to select first account by pressing Enter: {e}")
            try:
                print("⚠️ Trying fallback method: Arrow Down + Enter...")
                if account_field:
                    account_field.send_keys(Keys.ARROW_DOWN)
                    time.sleep(0.5)
                    account_field.send_keys(Keys.ENTER)
                    print("✓ Successfully selected first account using Arrow Down + Enter")
                else:
                    focused_element = driver.switch_to.active_element
                    focused_element.send_keys(Keys.ARROW_DOWN)
                    time.sleep(0.5)
                    focused_element.send_keys(Keys.ENTER)
                    print("✓ Successfully selected first account using Arrow Down + Enter on focused element")
            except Exception as e2:
                print(f"⚠️ All methods failed: {e2}")
                try:
                    print("⚠️ Last resort: Trying to click on dropdown items...")
                    dropdown_selectors = [
                        "//div[contains(@class, 'dropdown-menu')]//a[1]",
                        "//ul[contains(@class, 'dropdown')]//li[1]",
                        "//div[contains(@class, 'dropdown')]//div[1]",
                        "//*[contains(@class, 'dropdown-item')][1]",
                        "//*[contains(@class, 'list-item')][1]"
                    ]
                    for selector in dropdown_selectors:
                        try:
                            first_account = WebDriverWait(driver, 3).until(
                                EC.element_to_be_clickable((By.XPATH, selector))
                            )
                            first_account.click()
                            print(f"✓ Successfully clicked on first account using selector: {selector}")
                            break
                        except:
                            continue
                except Exception as e3:
                    print(f"⚠️ All methods failed to select first account: {e3}")

        print("\n" + "=" * 50)
        print("✓ NEW FUNCTIONALITY COMPLETED SUCCESSFULLY!")
        print("✓ Account dropdown opened by pressing Enter")
        print("✓ First account selected by pressing Enter again")
        print("=" * 50 + "\n")

        remarks_field = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "remarksid"))
        )
        remarks_field.clear()
        remarks_field.send_keys("This is an automated remark for PI.")
        time.sleep(5)
        print("✅ Remarks entered successfully.")

        # Barcode and quantity
        barcode_input = driver.find_element(By.ID, "barcodeField")
        barcode_input.clear()
        barcode_input.send_keys(barcode_purchase)
        barcode_input.send_keys(Keys.ENTER)

        quantity = random.randint(80, 200)
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

        # --- Discount (Dis%) 0 ---
        discount = random.randint(1, 50)
        print(f"Generated discount: {discount}%")
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

        # --- Discount (Dis%) 1 ---
        discount = random.randint(1, 50)
        try:
            discount_field = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.ID, "INDDISCOUNTRATE1"))
            )
            discount_field.clear()
            discount_field.send_keys(str(discount))
            time.sleep(2)
            print("✅ Discount entered.")
        except Exception as e:
            print(f"❌ Discount input not found: {e}")

        wait = WebDriverWait(driver, 10)
        save_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'SAVE') and contains(@class, 'btn-info')]")))
        save_button.click()

        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.accept()
            print("Alert accepted successfully.")
        except TimeoutException:
            print("No alert appeared after clicking SAVE.")

        import pyautogui
        time.sleep(10)
        pyautogui.press('esc')
        time.sleep(5)

        view_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'VIEW')]")))
        view_button.click()

        time.sleep(2)
        actions = ActionChains(driver)
        actions.send_keys(Keys.ENTER).perform()
        time.sleep(3)

        reset_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'RESET')]")))
        reset_btn.click()

        time.sleep(3)
        wait.until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(5)

        back_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'BACK')]")))
        back_btn.click()


    except Exception as e:
        import traceback
        print(f"\n❌ AN ERROR OCCURRED: {e}")
        traceback.print_exc()
        print("Current URL:", driver.current_url)


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

sales_tax_invoice(driver,
                  barcode_sales=11)


print("Keeping browser open for 30 seconds for observation...")
time.sleep(50)
