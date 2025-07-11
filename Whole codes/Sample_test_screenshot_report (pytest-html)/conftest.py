
# For generating report only




# import pytest
# import pytest_html
# from selenium import webdriver
# import os
# #Opens a Chrome browser and maximizes the window before the test starts.
# @pytest.fixture
# def driver(request):
#     # Initialize Chrome
#     driver = webdriver.Chrome()
#     driver.maximize_window()
# #yield pauses a function to give a value, then resumes later to finish remaining code—used in pytest fixtures to run setup before tests and cleanup after.
#     yield driver
#
#     # Quit browser after test
#     driver.quit()
#
#
# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     # This hook allows us to take a screenshot on failure
#     outcome = yield
#     rep = outcome.get_result()
#
#     if rep.when == "call" and rep.failed:
#         driver = item.funcargs.get("driver")
#         if driver:
#             screenshot_dir = os.path.join(os.getcwd(), "screenshots")
#             os.makedirs(screenshot_dir, exist_ok=True)
#             screenshot_path = os.path.join(screenshot_dir, f"{item.name}1.png")
#             driver.save_screenshot(screenshot_path)
#             # Attach to HTML report if pytest-html is installed
#             if hasattr(item.config, "_html"):
#                 extra = getattr(rep, "extra", [])
#                 extra.append(pytest_html.extras.image(screenshot_path))
#                 rep.extra = extra


# For generating report with screenshot

import pytest
import os
import time
import traceback
from selenium import webdriver
import pytest_html

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to add screenshot and error details to the HTML report on failure.
    """
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver")
        if driver:
            # Prepare screenshot directory
            screenshot_dir = os.path.join(os.getcwd(), "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)

            # Unique screenshot filename
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            screenshot_name = f"{item.name}_{timestamp}.png"
            screenshot_path = os.path.join(screenshot_dir, screenshot_name)

            # Take the screenshot
            driver.save_screenshot(screenshot_path)

            # Build error summary
            error_details = "".join(
                traceback.format_exception(
                    call.excinfo.type,
                    call.excinfo.value,
                    call.excinfo.tb
                )
            )

            # Attach to HTML report
            if hasattr(item.config, "_html"):
                extra = getattr(rep, "extra", [])

                # Embed image (will show inline in report)
                html_image = f'<div><img src="{screenshot_path}" alt="screenshot" style="width:600px;height:auto;" onclick="window.open(this.src)" /></div>'

                # Embed error text
                html_error = f"<div><pre>{error_details}</pre></div>"

                extra.append(pytest_html.extras.html(html_image))
                extra.append(pytest_html.extras.html(html_error))

                rep.extra = extra
