import pytest
import os

@pytest.fixture
def driver():
    from selenium import webdriver
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

# Add the hook to embed *all* errors after test completes
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    # If the test function used ErrorLogger and there were errors
    if rep.when == "call":
        logger = item.funcargs.get("logger", None)
        if logger and logger.has_errors():
            if hasattr(item.config, "_html"):
                extra = getattr(rep, "extra", [])
                for html_snippet in logger.get_report_entries():
                    import pytest_html
                    extra.append(pytest_html.extras.html(html_snippet))
                rep.extra = extra
