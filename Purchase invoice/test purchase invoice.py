from time import sleep

from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import random



def complete_automation(purchase_transaction_hovered=None):

    # Setup WebDriver

    global random, Main_function_productitem, account_field
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:


        print("Step 1: Opening login page...")
        driver.get("https://variantqa.webredirect.himshang.com.np/#/login?returnUrl=%2Fpages%2Fdashboard")
        time.sleep(3)

        print("Step 2: Entering credentials...")
        # Enter username and password
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="username"]'))
        )
        username_field.clear()
        username_field.send_keys("Sumita")

        password_field = driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="password"]')
        password_field.clear()
        password_field.send_keys("Tebahal1!")

        print("Step 3: Clicking Sign In...")
        # Click SIGN IN button
        sign_in_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign In')]"))
        )
        sign_in_button.click()

        print("Step 4: Checking for 'Already Logged In' popup...")
        # Handle "Already Logged In" popup if it appears
        try:
            popup = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Already Logged In')]"))
            )
            print("✓ 'Already Logged In' popup detected!")

            logout_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Logout')]"))
            )
            logout_button.click()
            print("✓ Clicked Logout button")
            time.sleep(2)

            # Re-login after logout
            sign_in_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign In')]"))
            )
            sign_in_button.click()
            print("✓ Re-logged in successfully")

        except Exception:
            print("✓ No 'Already Logged In' popup found, proceeding with normal login...")

        # ============ NAVIGATION TO PURCHASE TRANSACTION ============

          # Wait for dashboard to load completely
        print("Step 5: Waiting for dashboard to load...")
        time.sleep(3)  # Give additional time for page to fully load

        # Step 6: Click on "Transactions" menu
        print("Step 6: Clicking on 'Transactions' menu...")
        transactions_clicked = False

        # First, let's debug what's available on the page
        print("Step 6.1: Debugging available navigation elements...")
        try:
            # Find all navigation links
            nav_elements = driver.find_elements(By.XPATH, "//a | //div[@class*='nav'] | //span[@class*='nav']")
            print(f"Found {len(nav_elements)} potential navigation elements")

            visible_nav_texts = []
            for element in nav_elements[:15]:  # Check first 15 elements
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

        # Multiple selectors to try for Transactions menu
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

                # Use ActionChains for more reliable clicking
                actions = ActionChains(driver)
                actions.move_to_element(transactions_element).click().perform()

                print(f"✓ Successfully clicked on 'Transactions' using selector {i}")
                transactions_clicked = True
                time.sleep(2)
                break

            except Exception as e:
                print(f"  ✗ Selector {i} failed: {str(e)[:50]}...")
                continue

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

        # Step 8: Click on "Purchase Invoice" from the dropdown
        print("Step 8: Clicking on 'Purchase Invoice' from dropdown...")
        purchase_invoice_clicked = False

        # Multiple selectors for Purchase Invoice in dropdown
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

                # Click on Purchase Invoice
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
                # Find all elements containing "Purchase Invoice"
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

                # ============ NEW FUNCTIONALITY ADDED HERE ============

                # Step 9: Manually type in Invoice Number field
            print("Step 9: Manually typing in Invoice Number field...")
            import random
            import string

# Generate a random alphanumeric invoice number like "INV-X7K3L9"
            random_invoice = "INV-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            print(f"Generated Invoice Number: {random_invoice}")

            try:
                # Locate the invoice number input using its ID
                invoice_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "invoiceNO"))
                )
                invoice_field.clear()
                invoice_field.send_keys(random_invoice)
                print(f"✓ Successfully entered Invoice Number: {random_invoice}")
            except Exception as e:
                print(f"⚠️ Failed to enter Invoice Number: {e}")
# Step 10: Open Account dropdown by pressing Enter
            print("Step 10: Opening Account dropdown by pressing Enter...")

            try:
                # Find the Account field - try multiple selectors
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
                    # Click on the field first to focus it
                    account_field.click()
                    time.sleep(1)

                    # Press Enter to open dropdown
                    account_field.send_keys(Keys.ENTER)
                    print("✓ Successfully pressed Enter on Account field to open dropdown")
                    print("⏳ Waiting for dropdown list to load completely...")
                    time.sleep(3)  # Wait longer for dropdown to load completely

                else:
                    raise Exception("Could not find Account field")

            except Exception as e:
                print(f"⚠️ Failed to open Account dropdown using primary method: {e}")

                # Alternative approach - look for any input with "Account" placeholder
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

            # Step 11: Select first account by pressing Enter again
            print("Step 11: Selecting first account by pressing Enter again...")

            try:
                # Since dropdown is now open, press Enter again to select the first item
                if account_field:
                    account_field.send_keys(Keys.ENTER)
                    print("✓ Successfully pressed Enter again to select first account")
                    time.sleep(2)
                else:
                    # Try to find the focused element and press Enter
                    focused_element = driver.switch_to.active_element
                    focused_element.send_keys(Keys.ENTER)
                    print("✓ Successfully pressed Enter on focused element to select first account")
                    time.sleep(2)

            except Exception as e:
                print(f"⚠️ Failed to select first account by pressing Enter: {e}")

                # Fallback: Try arrow down then Enter
                try:
                    print("⚠️ Trying fallback method: Arrow Down + Enter...")
                    if account_field:
                        account_field.send_keys(Keys.ARROW_DOWN)
                        time.sleep(0.5)
                        account_field.send_keys(Keys.ENTER)
                        print("✓ Successfully selected first account using Arrow Down + Enter")
                    else:
                        # Use active element
                        focused_element = driver.switch_to.active_element
                        focused_element.send_keys(Keys.ARROW_DOWN)
                        time.sleep(0.5)
                        focused_element.send_keys(Keys.ENTER)
                        print("✓ Successfully selected first account using Arrow Down + Enter on focused element")

                except Exception as e2:
                    print(f"⚠️ All keyboard methods failed: {e2}")

                    # Last resort: Try clicking on dropdown items
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

#For remarks
            # wait = WebDriverWait(driver, 5)
            # remarks_field = wait.until(
            #     EC.presence_of_element_located((By.XPATH, "//textarea[@formcontrolname='remarks']")))
            #
            # # Enter text into Remarks
            # remarks_field.clear()
            # remarks_field.send_keys("This is a test remark.")
            #
           # #For product item section
        remarks_field = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, "remarksid"))
        )

        # Clear the field and type the remark
        remarks_field.clear()
        remarks_field.send_keys("This is an automated remark for PI.")
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

# # --- Discount ---
#                 discount = random.randint(1, 50)
#                 print(f"Generated discount:  {discount}%")
#                 discount_field_id= f"//table//tbody//tr[{row_index + 1}]//td[11]//input"  # Column 11 = Dis%
#
#                 try:
#                     discount_field = WebDriverWait(driver, 5).until(
#                         EC.element_to_be_clickable((By.ID, discount_field_id))
#                     )
#                     discount_field.clear()
#                     discount_field.send_keys(str(discount))
#                     print(f"✅ Discount {discount}% entered in row {row_index + 1}.")
#                 except Exception as e:
#                     print(f"❌ Discount input not found for row {row_index + 1}: {e}")



# # --- Discount (Dis%) ---
#             discount = random.randint(1, 50)
#             print(f"Generated discount: {discount}%")
#
#             try:
#                 discount_field = WebDriverWait(driver, 5).until(
#                     EC.element_to_be_clickable((By.ID, "INDDISCOUNTRATE0"))
#                 )
#                 discount_field.clear()
#                 discount_field.send_keys(str(discount))
#                 time.sleep(2)
#                 print("✅ Discount entered.")
#             except Exception as e:
#                 print(f"❌ Discount input not found: {e}")

           # # --- Discount (Dis%) ---
            #     discount = random.randint(1, 50)
            #     print(f"Generated discount: {discount}%")
            #
            #     try:
            #         discount_field = WebDriverWait(driver, 5).until(
            #             EC.element_to_be_clickable((By.ID, "INDDISCOUNTRATE0"))
            #         )
            #         discount_field.clear()
            #         discount_field.send_keys(str(discount))
            #         time.sleep(2)
            #         print("✅ Discount entered.")
            #     except Exception as e:
            #         print(f"❌ Discount input not found: {e}")

                # --- Discount (Dis%) ---
                # discount = random.randint(1, 50)
                # print(f"Generated discount: {discount}%")
                # discount_id = f"row_index"  # dynamic ID per row
                #
                # try:
                #     discount_field = WebDriverWait(driver, 5).until(
                #         EC.element_to_be_clickable((By.ID, discount_id))
                #     )
                #     discount_field.clear()
                #     discount_field.send_keys(str(discount))
                #     print(f"✅ Discount '{discount}%' entered in row {row_index + 1}.")
                # except Exception as e:
                #     print(f"❌ Could not enter discount in row {row_index + 1}: {e}")




        # can also do this to add product multiple as a times.

        #         """ barcodes = ["2020", "2021", "2022", "2023"]
        #         for code in barcodes:
        #             barcode_and_quantity_discount(driver, code)
        #         """

        # can call multiple times and add multiple products by adding barcode
        # Main_function_productitem(driver, "2020","INDDISCOUNTRATE0")
        # Main_function_productitem(driver,"2025","INDDISCOUNTRATE1")

        Main_function_productitem(driver, "2020")
        Main_function_productitem(driver,"2025")





# --- Discount (Dis%) ---
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



        # --- Discount (Dis%) ---
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


 # CLick on save button

        # Wait for the SAVE button and click it
        wait = WebDriverWait(driver, 10)
        save_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'SAVE') and contains(@class, 'btn-info')]")))
        save_button.click()

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

    except Exception as e:
        import traceback
        print(f"\n❌ AN ERROR OCCURRED: {e}")
        traceback.print_exc()
        print("Current URL:", driver.current_url)




    finally:

        # driver.quit()
        print("Automation finished!")

# Run the automation
if __name__ == "__main__":
    print("Starting Purchase Transaction automation...")
    complete_automation()
    print("Automation finished!")