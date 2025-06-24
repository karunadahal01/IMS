from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from datetime import datetime


# function
def complete_automation():
    # Setup WebDriver
    driver = webdriver.Chrome()  # Add path if needed
    driver.maximize_window()

    try:
        # ============ LOGIN SECTION ============
        print("Step 1: Opening login page...")
        driver.get("https://variantqa.webredirect.himshang.com.np/#/login?returnUrl=%2Fpages%2Fdashboard")
        time.sleep(2)  # Wait for the page to load(3)

        print("Step 2: Entering credentials...")
        # Enter username and password
        driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="username"]').send_keys("Sumita")
        driver .find_element(By.CSS_SELECTOR, 'input[formcontrolname="password"]').send_keys("Tebahal1!")

        print("Step 3: Clicking Sign In...")
        # Click SIGN IN button
        # again login button
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign In')]"))).click()
        print("Step 4: Checking for 'Already Logged In' popup...")
        # Check if "Already Logged In" popup appears
        try:
            # Wait for popup to appear (short wait)
            popup = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Already Logged In')]"))
            )
            print("✓ 'Already Logged In' popup detected!")

            # Click Logout button
            logout_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Logout')]"))
            )
            logout_button.click()
            print("✓ Clicked Logout button")
            time.sleep(2)  # Wait for logout to complete
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign In')]"))).click()
        except Exception as e:
            print("No 'Already Logged In' popup found, proceeding with normal login...")

        # ============ NAVIGATION SECTION ============
        print("Step 6: Navigating to Masters...")

        # Click Masters
        try:
            masters_link = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Masters')]"))
            )
            masters_link.click()
            print("✓ Clicked on Masters")
            time.sleep(2)
        except Exception as e:
            print(f"Could not click Masters: {e}")
            # Try hover approach
            try:
                masters_element = driver.find_element(By.XPATH, "//a[contains(text(), 'Masters')]")
                ActionChains(driver).move_to_element(masters_element).perform()
                time.sleep(1)
                masters_element.click()
                print("✓ Clicked on Masters using hover")
                time.sleep(2)
            except Exception as e2:
                print(f"Hover click also failed: {e2}")

        print("Step 7: Navigating to Inventory Info...")

        # Click Inventory Info
        try:
            inventory_info = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Inventory Info')]"))
            )
            inventory_info.click()
            print("✓ Clicked on Inventory Info")
            time.sleep(2)
        except Exception as e:
            print(f"Could not click Inventory Info: {e}")
            # Try alternative
            try:
                inventory_info = driver.find_element(By.LINK_TEXT, "Inventory Info")
                inventory_info.click()
                print("✓ Clicked on Inventory Info (alternative method)")
                time.sleep(2)
            except Exception as e2:
                print(f"Alternative method also failed: {e2}")

        print("Step 8: Navigating to Product Master...")

        # Click Product Master
        try:
            product_master = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Product Master')]"))
            )
            product_master.click()
            print("✓ Clicked on Product Master")
            time.sleep(3)
        except Exception as e:
            print(f"Could not click Product Master: {e}")
            # Try alternative
            try:
                product_master = driver.find_element(By.LINK_TEXT, "Product Master")
                product_master.click()
                print("✓ Clicked on Product Master (alternative method)")
                time.sleep(3)
            except Exception as e2:
                print(f"Alternative method also failed: {e2}")

        print("Step 9: Navigation completed successfully!")
        print("✓ You are now on the Product Master page")
        print("Current URL:", driver.current_url)


        # ============ ADD PRODUCT SECTION ============
        print("Step 10: Clicking 'Add Product' button...")
        try:
            # First, wait for and click the dropdown button
            add_product_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[@id='createDropdown' or contains(text(), 'Add Product')]"))
            )
            add_product_btn.click()
            print("✓ Clicked 'Add Product' button")
            time.sleep(2)  # Short wait for dropdown animation

            # ============ DROPDOWN SELECTION SECTION ============
            print("Step 11: Handling 'Add Product' dropdown...")

            # Option 1: Wait for dropdown items to load (if they're loaded dynamically)
            try:
                # Wait for at least one dropdown item to appear
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//ul[@class='dropdown-menu py-1 show']//li"))
                )

                # Now select the first option (or specific option if available)
                first_option = driver.find_element(By.XPATH, "//ul[@class='dropdown-menu py-1 show']//li[1]")
                first_option.click()
                print("✓ Selected first dropdown option")
                time.sleep(3)

            except Exception as e:
                print("Dropdown items not found, trying alternative approach...")

                # Option 2: Direct navigation via URL (if possible)
                try:
                    current_url = driver.current_url
                    if "/product-master" in current_url:
                        add_product_url = current_url.replace("/product-master", "/product-master/add")
                        driver.get(add_product_url)
                        print(f"✓ Directly navigated to add product page: {add_product_url}")
                        time.sleep(3)
                    else:
                        raise Exception("Not on product master page")

                except Exception as e2:
                    print(f"Direct navigation failed: {e2}")

                    # Option 3: JavaScript click alternative
                    try:
                        dropdown_button = driver.find_element(By.XPATH, "//button[@id='createDropdown']")
                        driver.execute_script("arguments[0].click();", dropdown_button)
                        time.sleep(1)

                        # Try to find and click the add option via JavaScript
                        add_option = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located(
                                (By.XPATH, "//a[contains(@href,'add') or contains(text(),'Add')]"))
                        )
                        driver.execute_script("arguments[0].click();", add_option)
                        print("✓ Used JavaScript to click add option")
                        time.sleep(3)

                    except Exception as e3:
                        print(f"All dropdown handling methods failed: {e3}")
                        print("❌ Could not access the Add Product form. Ending automation.")
                        return

        except Exception as e:
            print(f"✗ Could not click 'Add Product' button: {e}")
            return
        # ============ FORM FILLING SECTION ============
        print("Step 12: Starting form filling process...")

        # First, let's wait and check if we're on the correct page/form
        try:
            # Check if we can find the form or if we need to handle the dropdown differently
            form_present = False
            try:
                # Look for form indicators
                WebDriverWait(driver, 5).until(
                    EC.any_of(
                        EC.presence_of_element_located((By.XPATH,
                                                        "//h1[contains(text(), 'Add Product')] | //h2[contains(text(), 'Add Product')] | //div[contains(text(), 'Add Product')]")),
                        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter Item Name']")),
                        EC.presence_of_element_located((By.XPATH, "//label[contains(text(), 'Item Name')]"))
                    )
                )
                form_present = True
                print("✓ Form/Add Product page detected")
            except Exception:
                print("Form not detected, checking current page state...")
                print(f"Current URL: {driver.current_url}")

                # Try to click the dropdown again with a different approach
                try:
                    print("Attempting to re-trigger dropdown...")
                    # Look for the button that triggers dropdown and click it again
                    dropdown_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//button[@data-toggle='dropdown' and contains(text(), 'Add Product')]"))
                    )
                    dropdown_button.click()
                    time.sleep(2)

                    # Now try to click the dropdown option
                    add_product_link = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, "//a[contains(@href, 'add-product') or contains(text(), 'Add Product')]"))
                    )
                    add_product_link.click()
                    print("✓ Successfully clicked Add Product link")
                    time.sleep(3)
                    form_present = True
                except Exception as retry_error:
                    print(f"Retry dropdown click failed: {retry_error}")

            if not form_present:
                print("❌ Could not access the Add Product form. Ending automation.")
                return

        except Exception as e:
            print(f"Error checking form presence: {e}")

            ####################################Product master form to fillup data#############################

        def fill_product_form(driver):
            # Define product data (simplified)
            product_data = {
                'item_name': 'Test Product Name',
                'item_group': 'abcd11',
                'stock_unit': 'gm.',
                'description': 'This is a test product description',
                'purchase_price': '100',
                'sales_price': '150'
            }

            try:
                # ============ ITEM GROUP HANDLING ============
                print("Handling Item Group...")
                item_group_filled = False

                # Method 1: Try container first
                try:
                    item_group_container = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH,
                                                        "//div[contains(@class, 'form-group') and .//*[contains(text(), 'Item Group')]]"))
                    )

                    # Try direct input
                    try:
                        input_field = item_group_container.find_element(By.XPATH, ".//input")
                        input_field.clear()
                        input_field.send_keys(product_data['item_group'])
                        input_field.send_keys(Keys.RETURN)
                        print(f"✓ Item Group entered: {product_data['item_group']}")
                        item_group_filled = True
                    except:
                        pass

                    # Try select dropdown
                    if not item_group_filled:
                        try:
                            select_element = item_group_container.find_element(By.XPATH, ".//select")
                            select = Select(select_element)
                            try:
                                select.select_by_visible_text(product_data['item_group'])
                                print(f"✓ Item Group selected: {product_data['item_group']}")
                                item_group_filled = True
                            except:
                                if len(select.options) > 1:
                                    select.select_by_index(1)
                                    print("✓ Selected first available Item Group")
                                    item_group_filled = True
                        except:
                            pass

                    # Try clickable dropdown
                    if not item_group_filled:
                        try:
                            dropdown_button = item_group_container.find_element(
                                By.XPATH, ".//button[contains(@class, 'dropdown-toggle')]")
                            ActionChains(driver).move_to_element(dropdown_button).click().perform()
                            time.sleep(1)

                            try:
                                option = WebDriverWait(driver, 3).until(
                                    EC.element_to_be_clickable((By.XPATH,
                                                                f"//*[contains(@class, 'dropdown-menu')]//*[contains(text(), '{product_data['item_group']}')]"))
                                )
                                option.click()
                                print(f"✓ Selected Item Group from dropdown: {product_data['item_group']}")
                                item_group_filled = True
                            except:
                                try:
                                    first_option = driver.find_element(By.XPATH,
                                                                       "//*[contains(@class, 'dropdown-menu')]//*[contains(@class, 'dropdown-item')][1]")
                                    first_option.click()
                                    print("✓ Selected first available Item Group")
                                    item_group_filled = True
                                except:
                                    pass
                        except:
                            pass

                except Exception as e:
                    print(f"Initial Item Group container not found: {str(e)}")

                if not item_group_filled:
                    print("⚠️ Could not fill Item Group field")

                # ============ ITEM NAME ============
                print("Filling Item Name...")
                try:
                    item_name = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH,
                                                    "//input[contains(@placeholder, 'Item Name') or contains(@formcontrolname, 'itemName')]"))
                    )
                    item_name.clear()
                    item_name.send_keys(product_data['item_name'])
                    print(f"✓ Item Name entered: {product_data['item_name']}")
                except Exception as e:
                    print(f"⚠️ Could not fill Item Name: {str(e)}")

                # ============ STOCK UNIT ============
                print("Selecting Stock Unit...")
                try:
                    stock_unit = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH,
                                                    "//select[contains(@formcontrolname, 'stockUnit') or contains(@name, 'stockUnit')]"))
                    )
                    Select(stock_unit).select_by_visible_text(product_data['stock_unit'])
                    print(f"✓ Stock Unit selected: {product_data['stock_unit']}")
                except Exception as e:
                    print(f"⚠️ Could not select Stock Unit: {str(e)}")

                # ============ DESCRIPTION ============
                print("Filling Description...")
                try:
                    description = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH,
                                                    "//textarea[contains(@placeholder, 'Description') or contains(@formcontrolname, 'description')]"))
                    )
                    description.clear()
                    description.send_keys(product_data['description'])
                    print(f"✓ Description entered: {product_data['description']}")
                except Exception as e:
                    print(f"⚠️ Could not fill Description: {str(e)}")

                # ============ PRICE FIELDS WITH SCROLLING ============
                def scroll_to_element_and_fill(xpath, value, field_name):
                    try:
                        element = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, xpath))
                        )  # This parenthesis was missing
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                        time.sleep(0.5)  # Allow scroll to complete
                        element.clear()
                        element.send_keys(value)
                        print(f"✓ {field_name} entered: {value}")
                    except Exception as e:
                        print(f"⚠️ Could not fill {field_name}: {str(e)}")

                # Purchase Price
                print("Filling Purchase Price...")
                scroll_to_element_and_fill(
                    "//input[contains(@placeholder, 'Purchase Price') or contains(@formcontrolname, 'purchasePrice')]",
                    product_data['purchase_price'],
                    "Purchase Price"
                )

                # Sales Price
                print("Filling Sales Price...")
                scroll_to_element_and_fill(
                    "//input[contains(@placeholder, 'Sales Price') or contains(@formcontrolname, 'salesPrice')]",
                    product_data['sales_price'],
                    "Sales Price"
                )

                # ============ FORM SUBMISSION ============
                print("Submitting form...")
                try:
                    submit_btn = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH,
                                                    "//button[contains(text(), 'Save') or contains(text(), 'Submit') or contains(., 'SAVE')]"))
                    )
                    driver.execute_script("arguments[0].scrollIntoView();", submit_btn)
                    submit_btn.click()
                    print("✓ Form submitted successfully")

                    # Verify success
                    try:
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.XPATH,
                                                            "//*[contains(text(), 'success') or contains(text(), 'Success')]"))
                        )
                        print("✓ Success message verified")
                    except:
                        print("⚠️ Success message not detected")

                except Exception as e:
                    print(f"Form submission failed: {str(e)}")

            except Exception as e:
                print(f"Error in form filling: {str(e)}")
                raise


        # Keep browser open for observation
        print("Keeping browser open for observation...")
        time.sleep(30)  # Time to observe results

    except Exception as e:
        print(f"An error occurred: {e}")
        print("Current URL:", driver.current_url)
        # Take screenshot for debugging
        driver.save_screenshot(f"error_screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")

    finally:
        # Close browser (uncomment when ready)
        # driver.quit()
        print("Automation completed!")


# Run the automation
if __name__ == "__main__":
    print("Starting complete automation...")
    complete_automation()
    print("Automation finished!")