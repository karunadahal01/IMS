from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup WebDriver
driver = webdriver.Chrome()  # Add path if needed
driver.maximize_window()

# Open login page
driver.get("https://variantqa.webredirect.himshang.com.np/#/login?returnUrl=%2Fpages%2Fdashboard")
time.sleep(3)  # Wait for the page to load

# Enter username and password
driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="username"]').send_keys("Sumita")
driver.find_element(By.CSS_SELECTOR, 'input[formcontrolname="password"]').send_keys("Tebahal1!")

# Click SIGN IN



#use XPath
WebDriverWait(driver, 10).until( EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign In')]")) ).click()


# Css-Selector
#WebDriverWait(driver, 10).until( EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn-auth")) ).click()


# By class name
#WebDriverWait(driver, 10).until(
#    EC.element_to_be_clickable((By.CLASS_NAME, "btn-auth"))
#).click()


# Wait to observe result
time.sleep(200)

#  Close browser
# driver.quit()
