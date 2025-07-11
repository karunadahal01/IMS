import allure
import time
from wholefunction import Login,product_master,Purchase_invoice,Sales_tax_invoice

@allure.title("Test Flow of Oracle ERP")
def test_whole_function(driver):
    Login(
        driver,
        username="gedehim917@decodewp.com",
        password="Tebahal1!",
        link="https://velvet.webredirect.himshang.com.np/#/pages/dashboard"
    )

    product_master(driver,
                   product_item="Testing Item 1",
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
                   barcode_map="19",
                   barcode_unit="kg."

                   )

    Purchase_invoice(driver,
                     barcode_purchase=19)

    Sales_tax_invoice(driver,
                      barcode_sales=19)

print("Keeping browser open for 30 seconds for observation...")
time.sleep(50)