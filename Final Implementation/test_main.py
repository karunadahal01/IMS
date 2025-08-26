from webdriver_manager.core import driver
from selenium import webdriver
import Flow.test_login
from Flow import test_login

driver_ = webdriver.Chrome()

Flow.test_login.login(driver_, "gedehim917@decodewp.com",
                   "Tebahal1!",
                   "https://velvet.webredirect.himshang.com.np/#/pages/dashboard"
                    )
