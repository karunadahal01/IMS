from pages.login_page import LoginPage
from pages.purchase_invoice_page import PurchaseInvoicePage
from pages.product_master_page import ProductMasterPage
from utils.driver_utils import DriverManager
from config.settings import DEFAULT_USERNAME, DEFAULT_PASSWORD, BASE_URL

# Initialize driver
driver_manager = DriverManager()
driver = driver_manager.initialize_driver()

# Use page objects
#################################################################
login_page = LoginPage(driver)
login_page.login(DEFAULT_USERNAME, DEFAULT_PASSWORD, BASE_URL)
#################################################################
purchase_invoice_page = PurchaseInvoicePage(driver)
purchase_invoice_page.purchase_invoice(barcode_purchase = "8722")

################################################################
# product_page = ProductMasterPage(driver)
# product_page.product_master(
#                 product_item="IMS13",
#                 hs_code="309",
#                 unit="kg",
#                 item_type="Inventory Item",
#                 description="This is description by automation",
#                 category="N/A",
#                 short_name="ims",
#                 purchase_price="20",
#                 sales_price="40",
#                 barcode_map="9489",
#                 barcode_unit="kg")

# Cleanup


driver_manager.cleanup_driver()