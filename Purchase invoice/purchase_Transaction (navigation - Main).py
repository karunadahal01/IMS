from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime


def complete_automation(purchase_transaction_hovered=None):

    # Setup WebDriver
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
        #
        # if not transactions_clicked:
        #     print("⚠️ Trying alternative approach - searching for partial text match...")
        #     try:
        #         # Find all elements containing "Transaction"
        #         transaction_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Transaction')]")
        #         print(f"Found {len(transaction_elements)} elements containing 'Transaction'")
        #
        #         for element in transaction_elements:
        #             try:
        #                 element_text = element.text.strip()
        #                 if element_text == 'Transactions' and element.is_displayed():
        #                     actions = ActionChains(driver)
        #                     actions.move_to_element(element).click().perform()
        #                     print(f"✓ Clicked on 'Transactions' using fallback method")
        #                     transactions_clicked = True
        #                     time.sleep(2)
        #                     break
        #             except Exception:
        #                 continue
        #
        #     except Exception as e:
        #         print(f"⚠️ Fallback method also failed: {e}")

        # if not transactions_clicked:
        #     raise Exception("Could not find or click on 'Transactions' menu")
        #
        # # Step 7: Hover over "Purchase Transaction" to open dropdown
        # print("Step 7: Hovering over 'Purchase Transaction' to open dropdown...")
        # purchase_transaction_hovered = False
        #
        # # Multiple selectors for Purchase Transaction
        # purchase_selectors = [
        #     "//a[contains(text(), 'Purchase Transaction')]",
        #     "//div[contains(text(), 'Purchase Transaction')]",
        #     "//span[contains(text(), 'Purchase Transaction')]",
        #     "//*[text()='Purchase Transaction']",
        #     "//a[@routerlink and contains(text(), 'Purchase')]",
        #     "//*[contains(@class, 'nav') and contains(text(), 'Purchase Transaction')]"
        # ]
        #
        # for i, selector in enumerate(purchase_selectors, 1):
        #     try:
        #         print(f"  Trying Purchase Transaction selector {i}: {selector}")
        #         purchase_element = WebDriverWait(driver, 10).until(
        #             EC.element_to_be_clickable((By.XPATH, selector))
        #         )
        #
        #         # Use ActionChains to hover over the element to open dropdown
        #         actions = ActionChains(driver)
        #         actions.move_to_element(purchase_element).perform()
        #
        #         print(f"✓ Successfully hovered over 'Purchase Transaction' using selector {i}")
        #         purchase_transaction_hovered = True
        #         time.sleep(2)  # Wait for dropdown to appear
        #         break
        #
        #     except Exception as e:
        #         print(f"  ✗ Purchase selector {i} failed: {str(e)[:100]}...")
        #         continue

        if not purchase_transaction_hovered:
            print("⚠️ Trying alternative approach for Purchase Transaction hover...")
            try:
                # Find all clickable elements and search for Purchase Transaction
                # all_links = driver.find_elements(By.TAG_NAME, "a")

                #all_divs = driver.find_elements(By.TAG_NAME, "div")
                # all_spans = driver.find_elements(By.TAG_NAME, "span")

                #all_elements = all_links + all_divs + all_spans
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
            # "//a[contains(text(), 'Purchase Invoice')]",
            # "//div[contains(text(), 'Purchase Invoice')]",
            # "//span[contains(text(), 'Purchase Invoice')]",
            # "//*[text()='Purchase Invoice']",
            # "//li[contains(text(), 'Purchase Invoice')]",
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

        # if not purchase_invoice_clicked:
        #     raise Exception("Could not find or click on 'Purchase Invoice' from dropdown")
        #
        # # Step 9: Verify successful navigation to Purchase Invoice
        # print("Step 9: Verifying successful navigation to Purchase Invoice...")
        # try:
        #     # Wait for Purchase Invoice page to load
        #     WebDriverWait(driver, 15).until(
        #         EC.any_of(
        #             EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Purchase Invoice')]")),
        #             EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Invoice')]")),
        #             EC.presence_of_element_located((By.XPATH, "//h1 | //h2 | //h3")),
        #             EC.url_contains("purchase") or EC.url_contains("invoice")
        #         )
        #     )
        #
        #     current_url = driver.current_url
        #     print(f"✓ Successfully navigated to Purchase Invoice page")
        #     print(f"✓ Current URL: {current_url}")
        #
        #     # Print page title or main heading
        #     try:
        #         page_title = driver.find_element(By.TAG_NAME, "h1").text
        #         print(f"✓ Page title: {page_title}")
        #     except:
        #         try:
        #             page_title = driver.find_element(By.TAG_NAME, "h2").text
        #             print(f"✓ Page heading: {page_title}")
        #         except:
        #             print("✓ Purchase Invoice page loaded successfully")
        #
        # except Exception as e:
        #     print(f"⚠️ Could not verify page load: {e}")
        #
        #

        # Keep browser open for observation
        print("Keeping browser open for 30 seconds for observation...")
        time.sleep(30)

    except Exception as e:
        print(f"\n❌ AN ERROR OCCURRED: {e}")
        print(f"Current URL: {driver.current_url}")

        # Keep browser open for debugging
        print("Keeping browser open for debugging...")
        time.sleep(60)

    finally:
        # Uncomment the next line when you want to close the browser automatically
        # driver.quit()
        print("Automation finished!")

# Run the automation
if __name__ == "__main__":
    print("Starting Purchase Transaction automation...")
    complete_automation()
    print("Automation finished!")