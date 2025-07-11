# import allure
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.keys import Keys
# from selenium.common.exceptions import TimeoutException
# import time
#
# from conftest import driver
#
# ##########################################LOG IN###########################################################
# @allure.step("Logging in with username: {username} , password: {password} ")
# def Login(driver,username,password,link):
#
#     driver.maximize_window()
#     driver.get(link)
#     try:
#      with allure.step("Enter username"):
#         # Step 1: Enter credentials and click Sign In
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="username"]'))
#         ).send_keys(username)
#
#      with allure.step("Enter password"):
#
#         driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="password"]').send_keys(password)
#
#      with allure.step("Click Sign In button"):
#         sign_in_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]")
#         sign_in_btn.click()
#
#         # Step 2: Handle "Already Logged In" popup if present
#         try:
#
#          with allure.step("Check for 'Already Logged In' popup"):
#             logout_btn = WebDriverWait(driver, 20).until(
#                 EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Logout']]"))
#             )
#             print("✓ Already Logged In popup detected")
#
#             # Click Logout button
#             try:
#                 logout_btn.click()
#             except Exception:
#                 driver.execute_script("arguments[0].click();", logout_btn)
#             print("✓ Clicked Logout button")
#
#             time.sleep(8)
#             # Wait for the "Sign In" button to be clickable
#             sign_in_btn = WebDriverWait(driver, 10).until(
#                 EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign In')]"))
#             )
#
#             # Press Enter on the "Sign In" button
#             sign_in_btn.send_keys(Keys.ENTER)
#             print("✓ Clicked Sign In again after logout")
#
#         except TimeoutException:
#             with allure.step("No 'Already Logged In' popup detected - continuing"):
#                 pass
#             # print("ℹ️ No 'Already Logged In' popup detected — continuing without logout")
#
#         # Now you should be logged in fresh, add more actions here if needed
#
#     finally:
#         with allure.step("Login successful, waiting before next steps"):
#          def pytest_runtest_makereport(item, call):
#             outcome = yield
#             rep = outcome.get_result()
#             if rep.when == "call" and rep.failed:
#                 driver_fixture = item.funcargs.get("driver", None)
#                 if driver_fixture:
#                     allure.attach(driver_fixture.get_screenshot_as_png(),
#                                   name="screenshot_on_failure",
#                                   attachment_type=allure.attachment_type.PNG)
#             time.sleep(40)
#         # print("Login successfully")
#         # time.sleep(10)
#
#
# @allure.title("Test Login to Oracle ERP")
# def test_login(driver):
#     Login(
#         driver,
#         username="gedehim917@decodewp.com",
#         password="Tebahal1!",
#         link="https://velvet.webredirect.himshang.com.np/#/pages/dashboard")




#
# import allure
# import time
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.action_chains import ActionChains
#
#
# ##########################################LOG IN###########################################################
# @allure.step("Logging in with username: {username} , password: {password} ")
# def Login(driver, username, password, link):
#     try:
#         with allure.step("Maximize window and navigate to link"):
#             try:
#                 driver.maximize_window()
#                 driver.get(link)
#             except Exception as e:
#                 allure.attach(driver.get_screenshot_as_png(), name="Error_Navigate", attachment_type=allure.attachment_type.PNG)
#                 raise Exception(f"Failed to open link or maximize window: {e}")
#
#         with allure.step("Enter username"):
#             try:
#                 WebDriverWait(driver, 10).until(
#                     EC.presence_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="username"]'))
#                 ).send_keys(username)
#             except TimeoutException:
#                 allure.attach(driver.get_screenshot_as_png(), name="Username_Field_Timeout", attachment_type=allure.attachment_type.PNG)
#                 raise TimeoutException("Username field not found within timeout")
#             except Exception as e:
#                 raise Exception(f"Unexpected error entering username: {e}")
#
#         with allure.step("Enter password"):
#             try:
#                 driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="password"]').send_keys(password)
#             except NoSuchElementException:
#                 allure.attach(driver.get_screenshot_as_png(), name="Password_Field_NotFound", attachment_type=allure.attachment_type.PNG)
#                 raise NoSuchElementException("Password field not found on the page")
#             except Exception as e:
#                 raise Exception(f"Unexpected error entering password: {e}")
#
#         with allure.step("Click Sign In button"):
#             try:
#                 sign_in_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]")
#                 sign_in_btn.click()
#             except NoSuchElementException:
#                 allure.attach(driver.get_screenshot_as_png(), name="SignIn_Button_NotFound", attachment_type=allure.attachment_type.PNG)
#                 raise NoSuchElementException("Sign In button not found")
#             except ElementClickInterceptedException:
#                 driver.execute_script("arguments[0].click();", sign_in_btn)
#             except Exception as e:
#                 raise Exception(f"Unexpected error clicking Sign In: {e}")
#
#         with allure.step("Handle 'Already Logged In' popup if present"):
#             try:
#                 logout_btn = WebDriverWait(driver, 20).until(
#                     EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Logout']]"))
#                 )
#                 print("✓ Already Logged In popup detected")
#                 try:
#                     logout_btn.click()
#                 except Exception:
#                     driver.execute_script("arguments[0].click();", logout_btn)
#                 print("✓ Clicked Logout button")
#                 time.sleep(8)
#
#                 sign_in_btn = WebDriverWait(driver, 10).until(
#                     EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign In')]"))
#                 )
#                 sign_in_btn.send_keys(Keys.ENTER)
#                 print("✓ Clicked Sign In again after logout")
#             except TimeoutException:
#                 with allure.step("No 'Already Logged In' popup detected - continuing"):
#                     pass
#             except Exception as e:
#                 allure.attach(driver.get_screenshot_as_png(), name="Popup_Handle_Error", attachment_type=allure.attachment_type.PNG)
#                 raise Exception(f"Error handling 'Already Logged In' popup: {e}")
#
#         with allure.step("Login completed, wait before next steps"):
#             time.sleep(10)
#
#     except Exception as e:
#         allure.attach(driver.get_screenshot_as_png(), name="Login_Failed", attachment_type=allure.attachment_type.PNG)
#         raise Exception(f"Login process failed: {e}")
#     finally:
#         # Just an example if you wanted to always wait or cleanup
#         time.sleep(2)
#
# ########################################## PRODUCT MASTER ###########################################################
# @allure.step("Creating new product in Product Master")
# def product_master(driver, product_item, HS_code, unit, item_type,
#                    description, category, short_name, purchase_price, sales_price,
#                    alt_unit, conversion_factor,
#                    barcode_map, barcode_unit):
#
#     wait = WebDriverWait(driver, 10)
#
#     try:
#         with allure.step("Click on 'Masters' menu"):
#             try:
#                 Master_menu = driver.find_element(By.LINK_TEXT, "Masters")
#                 Master_menu.click()
#             except Exception as e:
#                 allure.attach(driver.get_screenshot_as_png(), name="Masters_Click_Failed", attachment_type=allure.attachment_type.PNG)
#                 raise Exception(f"Failed to click on 'Masters' menu: {e}")
#
#         with allure.step("Hover over 'Inventory Info'"):
#             try:
#                 inventory_info = wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Inventory Info")))
#                 ActionChains(driver).move_to_element(inventory_info).perform()
#                 time.sleep(3)
#             except Exception as e:
#                 allure.attach(driver.get_screenshot_as_png(), name="Hover_InventoryInfo_Failed", attachment_type=allure.attachment_type.PNG)
#                 raise Exception(f"Failed to hover over 'Inventory Info': {e}")
#
#         with allure.step("Click on 'Product Master'"):
#             product_master_link = wait.until(EC.visibility_of_element_located((By.LINK_TEXT, "Product Master")))
#             product_master_link.click()
#             time.sleep(5)
#
#         with allure.step("Click 'Add Product' button"):
#             add_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Add Product')]")))
#             add_btn.click()
#             time.sleep(5)
#
#         with allure.step("Click 'Add Product' label"):
#             add_label = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'Add Product')]")))
#             add_label.click()
#             time.sleep(3)
#
#         with allure.step("Zoom out for better visibility"):
#             driver.execute_script("document.body.style.zoom='80%'")
#             time.sleep(2)
#
#         with allure.step("Select Item Group"):
#             item_group_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='-- Press Enter For Item Group --']")))
#             item_group_input.click()
#             time.sleep(2)
#             item_group_input.send_keys(Keys.ENTER)
#             time.sleep(2)
#
#         with allure.step("Select Main Group"):
#             main_group_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//ng-select//input[@type='text']")))
#             main_group_input.click()
#             main_group_input.send_keys(Keys.ENTER, Keys.ENTER, Keys.ENTER)
#             time.sleep(4)
#
#         with allure.step("Click Ok button after Item Group selection"):
#             ok_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[.//span[normalize-space()='Ok']]")))
#             ok_button.click()
#             time.sleep(3)
#
#         with allure.step(f"Enter Item Name: {product_item}"):
#             item_name_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Enter Item Name']")))
#             item_name_input.clear()
#             item_name_input.send_keys(product_item)
#             driver.switch_to.active_element.send_keys(Keys.TAB)
#             time.sleep(2)
#
#         with allure.step(f"Enter HS Code: {HS_code}"):
#             driver.switch_to.active_element.send_keys(HS_code, Keys.TAB)
#             time.sleep(2)
#
#         with allure.step("Click Vatable checkbox"):
#             checkbox = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox' and contains(@class, 'ng-pristine')]")))
#             checkbox.click()
#             driver.switch_to.active_element.send_keys(Keys.TAB)
#             time.sleep(2)
#
#         with allure.step(f"Select Unit: {unit}"):
#             driver.switch_to.active_element.send_keys(unit, Keys.TAB)
#             time.sleep(2)
#
#         with allure.step(f"Select Item Type: {item_type}"):
#             driver.switch_to.active_element.send_keys(item_type, Keys.TAB)
#             time.sleep(2)
#
#         with allure.step(f"Enter Description: {description}"):
#             driver.switch_to.active_element.send_keys(Keys.TAB)
#             driver.switch_to.active_element.send_keys(description, Keys.TAB)
#             time.sleep(2)
#
#         with allure.step(f"Enter Category: {category}"):
#             driver.switch_to.active_element.send_keys(category, Keys.TAB)
#             time.sleep(2)
#
#         with allure.step(f"Enter Short Name: {short_name}"):
#             driver.switch_to.active_element.send_keys(short_name, Keys.TAB)
#             time.sleep(2)
#
#         with allure.step(f"Enter Purchase Price: {purchase_price}"):
#             price_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='number' and @placeholder='Enter Purchase Price']")))
#             price_input.clear()
#             price_input.send_keys(purchase_price)
#             time.sleep(2)
#
#         with allure.step(f"Enter Sales Price: {sales_price}"):
#             sales_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='number' and @placeholder='0']")))
#             sales_input.clear()
#             sales_input.send_keys(sales_price)
#             time.sleep(2)
#
#         with allure.step("Go to Alternate Unit tab"):
#             alternate_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='mat-tab-label-content' and normalize-space()='Alternate Unit']")))
#             alternate_tab.click()
#             time.sleep(2)
#
#         with allure.step(f"Select Alternate Unit: {alt_unit}"):
#             select_alt_unit = wait.until(EC.element_to_be_clickable((By.XPATH, "//select[contains(@class, 'ng-pristine')]")))
#             select_alt_unit.click()
#             driver.switch_to.active_element.send_keys(alt_unit, Keys.TAB)
#             time.sleep(2)
#
#         with allure.step(f"Enter Conversion Factor: {conversion_factor}"):
#             input_conversion = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='number' and contains(@class, 'ng-valid')]")))
#             input_conversion.clear()
#             input_conversion.send_keys(conversion_factor)
#             time.sleep(2)
#
#         with allure.step("Go to Barcode Mapping tab"):
#             barcode_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='mat-tab-label-content' and normalize-space()='Barcode Mapping']")))
#             barcode_tab.click()
#             time.sleep(2)
#
#         with allure.step(f"Enter Barcode: {barcode_map}"):
#             barcode_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter Bar Code']")))
#             barcode_input.clear()
#             barcode_input.send_keys(barcode_map)
#             driver.switch_to.active_element.send_keys(Keys.TAB)
#             time.sleep(2)
#
#         with allure.step(f"Select Barcode Unit: {barcode_unit}"):
#             select_barcode_unit = driver.find_element(By.CSS_SELECTOR, 'div.col-2.p-0 select')
#             select_barcode_unit.click()
#             driver.switch_to.active_element.send_keys(barcode_unit, Keys.TAB)
#             time.sleep(2)
#
#         with allure.step("Click Map button"):
#             map_button = wait.until(EC.element_to_be_clickable((By.ID, "map")))
#             map_button.click()
#             time.sleep(2)
#
#         with allure.step("Click Save to save the product"):
#             save_button = driver.find_element(By.XPATH, "//button[contains(text(),'SAVE')]")
#             save_button.click()
#             time.sleep(3)
#
#     except Exception as e:
#         allure.attach(driver.get_screenshot_as_png(), name="ProductMaster_Failed", attachment_type=allure.attachment_type.PNG)
#         raise Exception(f"Product Master flow failed: {e}")
#
import allure
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


########################################## CUSTOM EXCEPTION ###########################################################
class LoginError(Exception):
    """Custom exception for login related errors"""
    pass


########################################## LOG IN FUNCTION ###########################################################
@allure.step("Logging in with username: {username} , password: {password} ")
def Login(driver, username, password, link):
    try:
        ########################################## INPUT VALIDATION ##################################################
        if not isinstance(username, str) or not username.strip():
            raise LoginError("Invalid username: must be a non-empty string")
        if not isinstance(password, str) or not password.strip():
            raise LoginError("Invalid password: must be a non-empty string")
        if not isinstance(link, str) or not link.startswith("http"):
            raise LoginError("Invalid link: must be a valid URL string starting with http")

        with allure.step("Maximize window and navigate to link"):
            try:
                driver.maximize_window()
                driver.get(link)
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="Error_Navigate", attachment_type=allure.attachment_type.PNG)
                raise LoginError(f"Failed to open link or maximize window: {e}")

        with allure.step("Enter username"):
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[formcontrolname="username"]'))
                ).send_keys(username)
            except TimeoutException:
                allure.attach(driver.get_screenshot_as_png(), name="Username_Field_Timeout", attachment_type=allure.attachment_type.PNG)
                raise LoginError("Username field not found within timeout")
            except Exception as e:
                raise LoginError(f"Unexpected error entering username: {e}")

        with allure.step("Enter password"):
            try:
                driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="password"]').send_keys(password)
            except NoSuchElementException:
                allure.attach(driver.get_screenshot_as_png(), name="Password_Field_NotFound", attachment_type=allure.attachment_type.PNG)
                raise LoginError("Password field not found on the page")
            except Exception as e:
                raise LoginError(f"Unexpected error entering password: {e}")

        with allure.step("Click Sign In button"):
            try:
                sign_in_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]")
                sign_in_btn.click()
            except NoSuchElementException:
                allure.attach(driver.get_screenshot_as_png(), name="SignIn_Button_NotFound", attachment_type=allure.attachment_type.PNG)
                raise LoginError("Sign In button not found")
            except ElementClickInterceptedException:
                driver.execute_script("arguments[0].click();", sign_in_btn)
            except Exception as e:
                raise LoginError(f"Unexpected error clicking Sign In: {e}")

        with allure.step("Handle 'Already Logged In' popup if present"):
            try:
                logout_btn = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Logout']]"))
                )
                print("✓ Already Logged In popup detected")
                try:
                    logout_btn.click()
                except Exception:
                    driver.execute_script("arguments[0].click();", logout_btn)
                print("✓ Clicked Logout button")
                time.sleep(8)

                sign_in_btn = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign In')]"))
                )
                sign_in_btn.send_keys(Keys.ENTER)
                print("✓ Clicked Sign In again after logout")
            except TimeoutException:
                with allure.step("No 'Already Logged In' popup detected - continuing"):
                    pass
            except Exception as e:
                allure.attach(driver.get_screenshot_as_png(), name="Popup_Handle_Error", attachment_type=allure.attachment_type.PNG)
                raise LoginError(f"Error handling 'Already Logged In' popup: {e}")

        with allure.step("Login completed, wait before next steps"):
            time.sleep(10)

    except LoginError as e:
        allure.attach(driver.get_screenshot_as_png(), name="Login_Failed", attachment_type=allure.attachment_type.PNG)
        raise LoginError(f"Login process failed: {e}")
    finally:
        time.sleep(2)

@allure.title("Test Login to Oracle ERP")
def test_login(driver):
    Login(
        driver,
        username="gedehim917@decodewp.com",
        password="Tebahal12!",
        link="https://velvet.webredirect.himshang.com.np/#/pages/dashboard")
    #
    # product_master(driver,
    #                product_item="Testing1",
    #                HS_code="123",
    #                unit="kg.",
    #                item_type="Service Item",
    #                description="This is description",
    #                category="N/A",
    #                short_name="XYZ",
    #                purchase_price="120",
    #                sales_price="140",
    #                alt_unit="Each",
    #                conversion_factor="1000",
    #                barcode_map="2020",
    #                barcode_unit="kg."
    #
    #                )

