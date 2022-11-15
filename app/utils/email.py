from schemas.pydantic.product import ProductChange


def generate_html_change_product(product_change: ProductChange) -> str:
    data_change = ""

    for key, value in product_change.product_change.items():
        html_change = f"""
        <tr style="border: 1px solid black;
                   border-collapse: collapse;">
            <td style="border: 1px solid black;
                border-collapse: collapse;
                font-weight: bold;">
                {key}
            </td>
            <td style="border: 1px solid black;
                border-collapse: collapse;">
                {value}
            </td>
        </tr>"""
        data_change += html_change

    return f"""
        <html>
            <h1 style='text-align:left'>This is an update notification for Product</h1>
            <p>The product with id "{product_change.product_id}"
                and sku "{product_change.sku}"
                has been updated the user with id "{product_change.user_id}"</p>
            <p>Changes:</p>
            <table style="border: 1px solid black; border-collapse: collapse;">
                {data_change}
            </table>
        </html>
    """
