
from test_login import login

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

