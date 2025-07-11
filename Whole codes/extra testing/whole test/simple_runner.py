# simple_runner.py
# This file shows you exactly how to run your automation code

# First, you need to save your original code as 'main_automation.py'
# Then create this file to run it

import time
import sys
import os

# Import your functions (make sure your main file is named 'main_automation.py')
try:
    from main_automation import Login, product_master, Purchase_invoice, Sales_tax_invoice, driver

    print("✅ Successfully imported automation functions")
except ImportError as e:
    print(f"❌ Error importing functions: {e}")
    print("Make sure your main file is named 'main_automation.py' and in the same folder")
    sys.exit(1)

# =============================================================================
# CONFIGURATION SECTION - CHANGE THESE VALUES
# =============================================================================

# 1. LOGIN DETAILS (CHANGE THESE!)
LOGIN_URL = "https://velvet.webredirect.himshang.com.np/#/pages/dashboard"  # Replace with your app URL
USERNAME = "gedehim917@decodewp.com"  # Replace with your username
PASSWORD = "Tebahal1!"  # Replace with your password

# 2. PRODUCT DETAILS (CHANGE THESE!)
PRODUCT_CONFIG = {
    "product_item": "Test Product " + str(int(time.time())),  # Unique product name
    "HS_code": "12345678",
    "unit": "PCS",
    "item_type": "Finished Goods",
    "description": "Automated test product",
    "category": "Electronics",
    "short_name": "TEST-" + str(int(time.time()))[:4],
    "purchase_price": "100",
    "sales_price": "150",
    "alt_unit": "BOX",
    "conversion_factor": "10",
    "barcode_map": "123456789012" + str(int(time.time()))[-1],  # Unique barcode
    "barcode_unit": "PCS"
}

# 3. INVOICE DETAILS
CUSTOMER_NAME = "Test Customer"  # For sales invoice (optional)


# =============================================================================
# MAIN EXECUTION FUNCTIONS
# =============================================================================

def run_login_test():
    """Test only the login function"""
    print("\n🔐 Testing Login Function...")
    try:
        Login(USERNAME, PASSWORD, LOGIN_URL)
        print("✅ Login test completed successfully!")

        # Keep browser open for 10 seconds so you can see the result
        print("Browser will stay open for 10 seconds...")
        time.sleep(10)

    except Exception as e:
        print(f"❌ Login test failed: {e}")
    finally:
        try:
            driver.quit()
            print("🔄 Browser closed")
        except:
            pass


def run_product_test():
    """Test login + product creation"""
    print("\n🏭 Testing Product Creation...")
    try:
        # Step 1: Login
        print("Step 1: Logging in...")
        Login(USERNAME, PASSWORD, LOGIN_URL)
        time.sleep(3)

        # Step 2: Create Product
        print("Step 2: Creating product...")
        product_master(
            driver,
            PRODUCT_CONFIG["product_item"],
            PRODUCT_CONFIG["HS_code"],
            PRODUCT_CONFIG["unit"],
            PRODUCT_CONFIG["item_type"],
            PRODUCT_CONFIG["description"],
            PRODUCT_CONFIG["category"],
            PRODUCT_CONFIG["short_name"],
            PRODUCT_CONFIG["purchase_price"],
            PRODUCT_CONFIG["sales_price"],
            PRODUCT_CONFIG["alt_unit"],
            PRODUCT_CONFIG["conversion_factor"],
            PRODUCT_CONFIG["barcode_map"],
            PRODUCT_CONFIG["barcode_unit"]
        )

        print("✅ Product creation test completed successfully!")
        print(f"Product created: {PRODUCT_CONFIG['product_item']}")
        print(f"Barcode: {PRODUCT_CONFIG['barcode_map']}")

        # Keep browser open
        print("Browser will stay open for 15 seconds...")
        time.sleep(15)

    except Exception as e:
        print(f"❌ Product creation test failed: {e}")
    finally:
        try:
            driver.quit()
            print("🔄 Browser closed")
        except:
            pass


def run_purchase_test():
    """Test login + product + purchase invoice"""
    print("\n🛒 Testing Purchase Invoice...")
    try:
        # Step 1: Login
        print("Step 1: Logging in...")
        Login(USERNAME, PASSWORD, LOGIN_URL)
        time.sleep(3)

        # Step 2: Create Product
        print("Step 2: Creating product...")
        product_master(
            driver,
            PRODUCT_CONFIG["product_item"],
            PRODUCT_CONFIG["HS_code"],
            PRODUCT_CONFIG["unit"],
            PRODUCT_CONFIG["item_type"],
            PRODUCT_CONFIG["description"],
            PRODUCT_CONFIG["category"],
            PRODUCT_CONFIG["short_name"],
            PRODUCT_CONFIG["purchase_price"],
            PRODUCT_CONFIG["sales_price"],
            PRODUCT_CONFIG["alt_unit"],
            PRODUCT_CONFIG["conversion_factor"],
            PRODUCT_CONFIG["barcode_map"],
            PRODUCT_CONFIG["barcode_unit"]
        )
        time.sleep(3)

        # Step 3: Create Purchase Invoice
        print("Step 3: Creating purchase invoice...")
        Purchase_invoice(driver, PRODUCT_CONFIG["barcode_map"])

        print("✅ Purchase invoice test completed successfully!")

        # Keep browser open
        print("Browser will stay open for 15 seconds...")
        time.sleep(15)

    except Exception as e:
        print(f"❌ Purchase invoice test failed: {e}")
    finally:
        try:
            driver.quit()
            print("🔄 Browser closed")
        except:
            pass


def run_complete_test():
    """Run all tests: login + product + purchase + sales"""
    print("\n🎯 Running Complete Test Suite...")
    try:
        # Step 1: Login
        print("Step 1: Logging in...")
        Login(USERNAME, PASSWORD, LOGIN_URL)
        time.sleep(3)

        # Step 2: Create Product
        print("Step 2: Creating product...")
        product_master(
            driver,
            PRODUCT_CONFIG["product_item"],
            PRODUCT_CONFIG["HS_code"],
            PRODUCT_CONFIG["unit"],
            PRODUCT_CONFIG["item_type"],
            PRODUCT_CONFIG["description"],
            PRODUCT_CONFIG["category"],
            PRODUCT_CONFIG["short_name"],
            PRODUCT_CONFIG["purchase_price"],
            PRODUCT_CONFIG["sales_price"],
            PRODUCT_CONFIG["alt_unit"],
            PRODUCT_CONFIG["conversion_factor"],
            PRODUCT_CONFIG["barcode_map"],
            PRODUCT_CONFIG["barcode_unit"]
        )
        time.sleep(3)

        # Step 3: Create Purchase Invoice
        print("Step 3: Creating purchase invoice...")
        Purchase_invoice(driver, PRODUCT_CONFIG["barcode_map"])
        time.sleep(3)

        # Step 4: Create Sales Tax Invoice
        print("Step 4: Creating sales tax invoice...")
        Sales_tax_invoice(driver, PRODUCT_CONFIG["barcode_map"], CUSTOMER_NAME)

        print("🎉 Complete test suite finished successfully!")
        print(f"✅ Product created: {PRODUCT_CONFIG['product_item']}")
        print(f"✅ Purchase invoice created with barcode: {PRODUCT_CONFIG['barcode_map']}")
        print(f"✅ Sales tax invoice created for customer: {CUSTOMER_NAME}")

        # Keep browser open
        print("Browser will stay open for 20 seconds...")
        time.sleep(20)

    except Exception as e:
        print(f"❌ Complete test failed: {e}")
    finally:
        try:
            driver.quit()
            print("🔄 Browser closed")
        except:
            pass


# =============================================================================
# MENU SYSTEM
# =============================================================================

def show_menu():
    """Display the test menu"""
    print("\n" + "=" * 50)
    print("🚀 SELENIUM AUTOMATION TEST MENU")
    print("=" * 50)
    print("1. Test Login Only")
    print("2. Test Login + Product Creation")
    print("3. Test Login + Product + Purchase Invoice")
    print("4. Test Complete Flow (All Functions)")
    print("5. Exit")
    print("=" * 50)


def main():
    """Main function to run the tests"""
    print("🌟 Welcome to Selenium Automation Test Runner!")
    print("Make sure you have updated the configuration section above!")

    while True:
        show_menu()

        try:
            choice = input("\nEnter your choice (1-5): ").strip()

            if choice == "1":
                run_login_test()
            elif choice == "2":
                run_product_test()
            elif choice == "3":
                run_purchase_test()
            elif choice == "4":
                run_complete_test()
            elif choice == "5":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-5.")

        except KeyboardInterrupt:
            print("\n\n👋 Test interrupted by user. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

        # Ask if user wants to continue
        if choice in ["1", "2", "3", "4"]:
            continue_choice = input("\nDo you want to run another test? (y/n): ").strip().lower()
            if continue_choice != 'y':
                print("👋 Goodbye!")
                break


if __name__ == "__main__":
    # Check if configuration is updated
    if "your-application-url.com" in LOGIN_URL or "your_username" in USERNAME:
        print("⚠️  WARNING: Please update the configuration section at the top of this file!")
        print("   - Change LOGIN_URL to your actual application URL")
        print("   - Change USERNAME and PASSWORD to your actual credentials")
        print("   - Update product details if needed")
        print("\nDo you want to continue anyway? (y/n): ", end="")
        if input().strip().lower() != 'y':
            print("👋 Please update the configuration and run again.")
            sys.exit(1)

    main()