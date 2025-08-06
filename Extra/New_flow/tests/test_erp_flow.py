# tests/test_erp_flow.py

import time
import allure
import pytest
from pages.login_page import LoginPage
from pages.product_master_page import ProductMasterPage
from pages.purchase_invoice_page import PurchaseInvoicePage
from pages.sales_tax_invoice_page import SalesTaxInvoicePage
from pages.purchase_return_page import PurchaseReturnPage
from pages.sales_return_page import SalesReturnPage
from config.settings import DEFAULT_USERNAME, DEFAULT_PASSWORD, BASE_URL


@allure.feature("Test ERP Flow Creation")
class TestERPFlowCreation:
    """Test class for ERP flow creation scenarios."""

    @allure.story("User Login")
    def test_login(self, driver):
        """Test case for user login."""
        with allure.step("Login to the application"):
            login_page = LoginPage(driver)
            login_page.login(DEFAULT_USERNAME, DEFAULT_PASSWORD, BASE_URL)

    @allure.story("Product Master Creation")
    def test_product_master(self, driver):
        """Test case for creating product master."""
        with allure.step("Creating new product item"):
            # Login
            login_page = LoginPage(driver)
            login_page.login(DEFAULT_USERNAME, DEFAULT_PASSWORD, BASE_URL)

            # Create product master
            product_page = ProductMasterPage(driver)
            product_page.create_product_master(
                product_item="tested1",
                HS_code="123",
                unit="kg.",
                item_type="Service Item",
                description="This is description",
                category="N/A",
                short_name="XYZ",
                purchase_price="120",
                sales_price="140",
                alt_unit="Each",
                conversion_factor="1000",
                barcode_map="555",
                barcode_unit="kg."
            )

    @allure.story("Purchase Invoice Creation")
    def test_purchase_invoice(self, driver):
        """Test case for creating purchase invoice."""
        with allure.step("PURCHASE a product item"):
            # Login
            login_page = LoginPage(driver)
            login_page.login(DEFAULT_USERNAME, DEFAULT_PASSWORD, BASE_URL)

            # Create product master
            product_page = ProductMasterPage(driver)
            product_page.create_product_master(
                product_item="Tested99",
                HS_code="123",
                unit="kg.",
                item_type="Service Item",
                description="This is description",
                category="N/A",
                short_name="XYZ",
                purchase_price="120",
                sales_price="140",
                alt_unit="Each",
                conversion_factor="1000",
                barcode_map="143",
                barcode_unit="kg."
            )

            # Create purchase invoice
            purchase_page = PurchaseInvoicePage(driver)
            purchase_page.create_purchase_invoice(barcode_purchase=666)

    @allure.story("testing small flow")
    def test_flow(self, driver):
        """Test case for creating sales tax invoice."""
        with allure.step("Sales a product item"):
            # Login
            login_page = LoginPage(driver)
            login_page.login(DEFAULT_USERNAME, DEFAULT_PASSWORD, BASE_URL)
            #
            # Create product master
            product_page = ProductMasterPage(driver)
            product_page.create_product_master(
                product_item="bb",
                HS_code="123",
                unit="Each",
                item_type="Inventory Item",
                description="This is description",
                category="N/A",
                short_name="XYZ",
                purchase_price="120",
                sales_price="140",
                alt_unit="kg",
                conversion_factor="1000",
                barcode_map="82",
                barcode_unit="Each"
            )

            # Create purchase invoice
            purchase_page = PurchaseInvoicePage(driver)
            purchase_page.create_purchase_invoice(barcode_purchase=82)

            # Create sales tax invoice
            sales_page = SalesTaxInvoicePage(driver)
            sales_page.create_sales_tax_invoice(barcode_sales=82)

    @allure.story("Purchase Return")
    def test_purchase_return(self, driver):
        """Test case for purchase return."""
        with allure.step("Return a purchase invoice"):
            # Login
            login_page = LoginPage(driver)
            login_page.login(DEFAULT_USERNAME, DEFAULT_PASSWORD, BASE_URL)

            # Create purchase return
            purchase_return_page = PurchaseReturnPage(driver)
            purchase_return_page.create_purchase_return(
                remarks="Testing Purchase Return by automation."
            )

    @allure.story("Sales Return Full")
    def test_sales_return(self, driver):
        """Test case for full sales return."""
        with allure.step("sales return full"):
            # Login
            login_page = LoginPage(driver)
            login_page.login(DEFAULT_USERNAME, DEFAULT_PASSWORD, BASE_URL)

            # Create sales tax invoice first
            sales_page = SalesTaxInvoicePage(driver)
            sales_page.create_sales_tax_invoice(barcode_sales=2222)

            # Create full sales return
            sales_return_page = SalesReturnPage(driver)
            sales_return_page.create_sales_return_full()

    @allure.story("Sales Return Partial")
    def test_sales_return_partial(self, driver):
        """Test case for partial sales return."""
        with allure.step("sales return partial"):
            # Login
            login_page = LoginPage(driver)
            login_page.login(DEFAULT_USERNAME, DEFAULT_PASSWORD, BASE_URL)

            # Create sales tax invoice first
            sales_page = SalesTaxInvoicePage(driver)
            sales_page.create_sales_tax_invoice(barcode_sales=2222)

            # Create partial sales return
            sales_return_page = SalesReturnPage(driver)
            sales_return_page.create_sales_return_partial(return_barcode="9999")

    def teardown_method(self):
        """Keep browser open for observation."""
        print("Keeping browser open for 30 seconds for observation...")
        time.sleep(30)