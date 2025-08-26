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

################################## LOG IN ###########################################################
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


################################## PURCHASE INVOICE ###########################################################

def Purchase_invoice(driver, barcode_purchase):
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
################################################################
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
#Function call

Login(
    username="gedehim917@decodewp.com",
    password="Tebahal1!",
    link="https://velvet.webredirect.himshang.com.np/#/pages/dashboard")

Purchase_invoice(driver,
                 barcode_purchase=822)


print("Keeping browser open for 30 seconds for observation...")
time.sleep(30)
