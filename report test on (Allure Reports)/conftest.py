# conftest.py
import pytest
import allure
from selenium import webdriver

@pytest.fixture(scope="function")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

# Automatically attach screenshot if a test fails
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver_fixture = item.funcargs.get("driver", None)
        if driver_fixture:
            allure.attach(driver_fixture.get_screenshot_as_png(),
                          name="screenshot_on_failure",
                          attachment_type=allure.attachment_type.PNG)
