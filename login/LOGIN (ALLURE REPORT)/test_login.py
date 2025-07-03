import allure
from login import Login

@allure.title("Test Login to Oracle ERP")
def test_login(driver):
    Login(
        driver,
        username="gedehim917@decodewp.com",
        password="Tebahal1!",
        link="https://velvet.webredirect.himshang.com.np/#/pages/dashboard"
    )
