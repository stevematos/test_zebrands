from app.schemas.pydantic.product import ProductChange
from app.utils.email import generate_html_change_product


def test_generate_html_change_product():
    product_change = ProductChange(
        email="test",
        user_id=1,
        sku="TEST123",
        product_id=1,
        product_change={"price": 13.1, "name": "chocolate"},
    )

    actual = generate_html_change_product(product_change)
    expected = """<html>
            <h1 style='text-align:left'>This is an update notification for Product</h1>
            <p>The product with id "1"
                and sku "TEST123"
                has been updated the user with id "1"</p>
            <p>Changes:</p>
            <table style="border: 1px solid black; border-collapse: collapse;">

        <tr style="border: 1px solid black;
                   border-collapse: collapse;">
            <td style="border: 1px solid black;
                border-collapse: collapse;
                font-weight: bold;">
                price
            </td>
            <td style="border: 1px solid black;
                border-collapse: collapse;">
                13.1
            </td>
        </tr>
        <tr style="border: 1px solid black;
                   border-collapse: collapse;">
            <td style="border: 1px solid black;
                border-collapse: collapse;
                font-weight: bold;">
                name
            </td>
            <td style="border: 1px solid black;
                border-collapse: collapse;">
                chocolate
            </td>
        </tr>
            </table>
        </html>"""
    assert actual.strip() == expected.strip()
