# error_logger.py
import os
import time
import traceback

class ErrorLogger:
    def __init__(self, driver):
        self.driver = driver
        self.errors = []

    def log_error(self, note, exception_obj):
        # Create screenshot folder
        screenshot_dir = os.path.join(os.getcwd(), "screenshots")
        os.makedirs(screenshot_dir, exist_ok=True)

        # Take screenshot
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{note}_{timestamp}.png"
        screenshot_path = os.path.join(screenshot_dir, filename)
        self.driver.save_screenshot(screenshot_path)

        # Store error detail
        error_text = "".join(
            traceback.format_exception(
                type(exception_obj),
                exception_obj,
                exception_obj.__traceback__
            )
        )

        self.errors.append({
            "note": note,
            "screenshot": screenshot_path,
            "error": error_text
        })

    def has_errors(self):
        return len(self.errors) > 0

    def get_report_entries(self):
        """
        Returns a list of HTML snippets to attach to pytest-html report.
        """
        entries = []
        for e in self.errors:
            html = f"""
            <div>
                <h4>{e['note']}</h4>
                <img src="{e['screenshot']}" style="width:600px;height:auto;" onclick="window.open(this.src)">
                <pre>{e['error']}</pre>
            </div>
            """
            entries.append(html)
        return entries
