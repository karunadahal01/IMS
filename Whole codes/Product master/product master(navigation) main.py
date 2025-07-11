from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime

#function
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
        driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="password"]').send_keys("Tebahal1!")

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
# again login button
       # WebDriverWait(driver, 10).until(
          #  EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign In')]"))).click()



        # ============ NAVIGATION SECTION ============
        print("Step 6: Navigating to Masters...")

        # Click Masters
        try:
            masters_link = WebDriverWait(driver, 5).until( #(10)
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
            inventory_info = WebDriverWait(driver, 5).until( #10
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
            product_master = WebDriverWait(driver, 5).until( #10
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
        print("Step 9: Clicking 'Add Product' button...")
        try:
            add_product_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add Product')]"))
            )
            add_product_btn.click()
            print("✓ Clicked 'Add Product' button")
            time.sleep(3)

        except Exception as e:
            print(f"✗ Could not click 'Add Product' button: {e}")

        # Keep browser open for observation
        print("Keeping browser open for observation...")
        time.sleep(200)  # Extended time to observe

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