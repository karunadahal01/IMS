from pages.login_page import LoginPage
from pages.purchase_invoice_page import PurchaseInvoicePage
from pages.product_master_page import ProductMasterPage
from utils.driver_utils import DriverManager
from config.settings import DEFAULT_USERNAME, DEFAULT_PASSWORD, BASE_URL
from pages.purchase_return_page import PurchaseReturnPage
from pages.sales_tax_invoice_page import SalesTaxInvoicePage
from pages.sales_return_page import SalesReturnPage

# Initialize driver

driver_manager = DriverManager()
driver = driver_manager.initialize_driver()

# Use page objects
#################################################################
login_page = LoginPage(driver)
login_page.login(DEFAULT_USERNAME, DEFAULT_PASSWORD, BASE_URL)

###################################################################

# purchase_return = PurchaseReturnPage(driver)
# purchase_return.purchase_return(Remarks='This is purchase return by automation testing')

#################################################################
# Sales_invoice = SalesTaxInvoicePage(driver)
# Sales_invoice.create_sales_tax_invoice(barcode_sales ='822')
#####################################################################

# purchase_invoice_page = PurchaseInvoicePage(driver)
# purchase_invoice_page.purchase_invoice(barcode_purchase = "8722")

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

##################################################################################################

# sales_return = SalesReturnPage(driver)
# sales_return.create_sales_return_full()

###########################################################################################
sales_return_partial = SalesReturnPage(driver)
sales_return_partial.create_sales_return_partial(barcode=822)
############################################################################################
# Cleanup
driver_manager.cleanup_driver()