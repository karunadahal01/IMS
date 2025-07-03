import pytest
from error_logger import ErrorLogger
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def test_collect_multiple_errors(driver):
    logger = ErrorLogger(driver)
    driver.get("https://www.google.com")

    # First error
    try:
        driver.find_element(By.ID, "does-not-exist").click()
    except Exception as e:
        logger.log_error("Missing element", e)

    # Second error
    try:
        driver.find_element(By.NAME, "q").send_keys("Selenium" + Keys.ENTER)
        driver.find_element(By.ID, "another-fake-id").click()
    except Exception as e:
        logger.log_error("Second missing element", e)

    # Third error
    try:
        driver.find_element(By.TAG_NAME, "footer").click()
    except Exception as e:
        logger.log_error("Footer click failed", e)

    # At the end: fail once if any errors
    if logger.has_errors():
        # This will appear in the report
        errors_text = "\n\n".join(
            f"{e['note']}\n{e['error']}" for e in logger.errors
        )
        pytest.fail(f"Errors captured:\n\n{errors_text}")
