from test_Flow_main import *


# ##########################################################################################################################
# Test case first ( Login)

def test_login(self):
        allure.step("Login to the application")
        self.login("gedehim917@decodewp.com",
                   "Tebahal1!",
                   "https://velvet.webredirect.himshang.com.np/#/pages/dashboard")

# ##########################################################################################################################
# Test case second (login, Product Master)

def test_product_master(self):
        allure.step("Creating new product item")
        self.login("gedehim917@decodewp.com",
                   "Tebahal1!",
                   "https://velvet.webredirect.himshang.com.np/#/pages/dashboard")
        self.product_master(
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
                       barcode_unit="kg.")

# ##########################################################################################################################
# Test case Third (Login,Product master, Purchase Invoice)

def test_purchase_invoice(self):
        allure.step("purchasing a product item")
        self.login("gedehim917@decodewp.com",
                   "Tebahal1!",
                   "https://velvet.webredirect.himshang.com.np/#/pages/dashboard")
        self.product_master(
            product_item="Tested2",
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
            barcode_map="666",
            barcode_unit="kg.")

        self.Purchase_invoice(
                         barcode_purchase=666)
##########################################################################################################################
# Test case Fourth (Login,Product master, Sales Tax Invoice)

def test_sales_tax_invoice(self):
        allure.step("sales a product item")
        self.login("gedehim917@decodewp.com",
                   "Tebahal1!",
                   "https://velvet.webredirect.himshang.com.np/#/pages/dashboard")
        self.product_master(
            product_item="Test3",
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
            barcode_map="777",
            barcode_unit="kg.")

        self.Purchase_invoice(
                         barcode_purchase=777)

        self.sales_tax_invoice(
                        barcode_sales=777)

#######################################################################################################################
# Test case Fifth (Login,purchase, purchase  Return)
def test_purchase_return(self):
    allure.step("Return a purchase invoice")
    self.login("gedehim917@decodewp.com",
               "Tebahal1!",
               "https://velvet.webredirect.himshang.com.np/#/pages/dashboard")

    self.purchase_return(Remarks="Testing Purchase Return by automation.")

#####################################################################################################################3
# Test case Sixth (Login,sales, sales  Return full)
def test_sales_return_full(self):
        allure.step("sales return full")
        self.login("gedehim917@decodewp.com",
                   "Tebahal1!",
                   "https://velvet.webredirect.himshang.com.np/#/pages/dashboard")

        self.sales_tax_invoice(
            barcode_sales=777)
        self.sales_return_full(self)

#######################################################################################################################
# Test case Sixth (Login,sales, sales  Return partial)

def test_sales_return_Partial(self):
        allure.step("sales return partial")
        self.login("gedehim917@decodewp.com",
                   "Tebahal1!",
                   "https://velvet.webredirect.himshang.com.np/#/pages/dashboard")

        self.sales_tax_invoice(barcode_sales=777)
        self.sales_return_partial( return_barcode="15")









