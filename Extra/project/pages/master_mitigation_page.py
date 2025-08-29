import logging
from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

logger = logging.getLogger(__name__)


class MasterMitigtionPage(BasePage):
    def customer(self):


        # Click on "Utilities"
        try:
            utilities_menu = self.driver.find_element(By.LINK_TEXT, "Utilities")
            utilities_menu.click()
            print("Clicked on 'Utilities'")
        except Exception as e:
            print("Error clicking 'Utilities':", e)
            time.sleep(10)

        # Click on "Migration"
        try:
            migration_menu = self.driver.find_element(By.LINK_TEXT, "Migration")
            migration_menu.click()
            print("Clicked on 'Migration'")
        except Exception as e:
            print("Error clicking 'Migration':", e)
            time.sleep(10)

        # Click on "Master Migration"
        try:
            master_migration_menu = self.driver.find_element(By.LINK_TEXT, "Master Migration")
            master_migration_menu.click()
            time.sleep(4)
            body = self.driver.find_element(By.TAG_NAME, 'body')
            # Click the body
            body.click()
            print("Clicked on 'Master Migration'")
        except Exception as e:
            print("Error clicking 'Master Migration':", e)
            time.sleep(10)

        # CLick on upload sheet
        try:
            # Wait until the element is clickable
            upload_sheet_link = WebDriverWait(self.driver, 10).until(
                ec.element_to_be_clickable((By.CSS_SELECTOR, 'a.nav-link[href="#upload-sheet"]'))
            )
            upload_sheet_link.click()
            print("Clicked on 'Upload Sheet'")
        except Exception as e:
            print("Error clicking 'Upload Sheet':", e)
            time.sleep(10)

        # select customer master
        try:
            # # Optional: wait or continue other actions
            time.sleep(10)
            body = self.driver.find_element(By.TAG_NAME, 'body')
            actions = ActionChains(self.driver)
            # actions.click(body).send_keys(Keys.TAB).send_keys(Keys.TAB).perform()
            actions.click(body).send_keys(Keys.TAB).perform()
            self.driver.switch_to.active_element.send_keys("Customer Master")


        except Exception as e:
            print("Error selecting 'Customer Master':", e)
            time.sleep(10)

        # SElecting file
        time.sleep(3)
        # Upload the file
        file_input = self.driver.find_element(By.CSS_SELECTOR, 'input[type="file"]')
        file_input.send_keys(
            r"C:\Users\karun\Downloads\Customer Master Sample.xlsx")  # Use raw string to avoid path errors

        # Optional wait for the file to be processed
        time.sleep(1)

        # Click the "Upload File" button
        upload_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Upload File')]")
        upload_button.click()

        time.sleep(8)


        ###########################################################################################################################################
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)


        # Wait for upload to complete (if any processing)
        time.sleep(3)


        # CLick on upload status
        try:
            # Wait until the element is clickable
            upload_status_link = WebDriverWait(self.driver, 10).until(
                ec.element_to_be_clickable((By.CSS_SELECTOR, 'a.nav-link[href="#upload-status"]'))
            )
            upload_status_link.click()
            print("Clicked on 'Upload Status'")
        except Exception as e:
            print("Error clicking 'Upload Status':", e)
            time.sleep(10)

            # select customer master
        try:

            time.sleep(10)
            body = self.driver.find_element(By.TAG_NAME, 'body')
            actions = ActionChains(self.driver)
            # actions.click(body).send_keys(Keys.TAB).send_keys(Keys.TAB).perform()
            actions.click(body).send_keys(Keys.TAB).perform()
            self.driver.switch_to.active_element.send_keys("Customer Master")

        except Exception as e:
            print("Error selecting 'Customer Master':", e)
            time.sleep(10)

        time.sleep(5)

        # Click the "Download_Status" button
        download_status = self.driver.find_element(By.XPATH, "//button[contains(text(), ' Download Status ')]")
        download_status.click()





