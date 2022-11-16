from unittest.mock import create_autospec, patch

import pytest
from config.exceptions import ProductDuplicated
from models import Product
from schemas.graphql.product import CreateProductResponse
from schemas.pydantic.product import ProductSchema
from services.product import add_product
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session


@pytest.mark.parametrize(
    ("sku", "is_duplicated"),
    (
        ("test123", False),
        ("NoResultFound", False),
        ("duplicate", True),
    ),
)
@patch("services.product.create_product")
@patch("services.product.get_product_by_sku")
def test_add_product(
    mock_get_product_by_sku,
    mock_create_product,
    sku,
    is_duplicated,
):
    db = create_autospec(Session)

    product_dict = {
        "sku": sku,
        "name": "test",
        "price": 13,
        "brand": "test brand",
    }

    product = ProductSchema(**product_dict)

    def get_product_by_sku_effect(db, sku, **kwargs):
        if sku == "test123":
            return None
        elif sku == "duplicate":
            return Product(sku=sku)
        elif sku == "NoResultFound":
            raise NoResultFound()

    mock_get_product_by_sku.side_effect = get_product_by_sku_effect
    mock_create_product.return_value = Product(**product_dict)

    if is_duplicated:
        with pytest.raises(ProductDuplicated):
            add_product(db, product)
    else:
        actual = add_product(db, product)

        mock_get_product_by_sku.assert_called_once_with(db, sku)
        expected = CreateProductResponse(**product_dict)

        assert expected == actual
