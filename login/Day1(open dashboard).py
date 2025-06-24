# Import Necessary Files

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Open Link in given driver: Chrome
driver = webdriver.Chrome()
driver.get("https://variantqa.webredirect.himshang.com.np/#/login?returnUrl=%2Fpages%2Fdashboard")
print("Open Browser")

#title is shown of the given page
title = driver.title
print(title)

"""
# maximizing & Minimizing window
driver.maximize_window()
print("maximize Window")

driver.minimize_window()
print("Minimize Window")

"""
# Enter username
Username=driver.find_element(By.CSS_SELECTOR,'input[formcontrolname="username"]')
Username.send_keys("Sumita")

# Enter Password
password = driver.find_element(By.CSS_SELECTOR,'input[formcontrolname="password"]')
password.send_keys("Tebahal1!")

# Click on button
driver.find_element(By.XPATH, "//button[contains(text(), 'SIGN IN')]").click()
time.sleep(300)