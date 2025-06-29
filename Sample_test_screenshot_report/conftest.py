import pytest
import pytest_html
from selenium import webdriver
import os
#Opens a Chrome browser and maximizes the window before the test starts.
@pytest.fixture
def driver(request):
    # Initialize Chrome
    driver = webdriver.Chrome()
    driver.maximize_window()
#yield pauses a function to give a value, then resumes later to finish remaining code—used in pytest fixtures to run setup before tests and cleanup after.
    yield driver

    # Quit browser after test
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # This hook allows us to take a screenshot on failure
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            screenshot_dir = os.path.join(os.getcwd(), "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)
            screenshot_path = os.path.join(screenshot_dir, f"{item.name}1.png")
            driver.save_screenshot(screenshot_path)
            # Attach to HTML report if pytest-html is installed
            if hasattr(item.config, "_html"):
                extra = getattr(rep, "extra", [])
                extra.append(pytest_html.extras.image(screenshot_path))
                rep.extra = extra
