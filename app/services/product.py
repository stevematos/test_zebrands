from config.exceptions import ProductDuplicated, ProductNotFound
from models import Product, ProductTracking
from queries.product import (
    create_product,
    create_product_tacking,
    delete_product,
    get_product_by_sku,
    update_product,
)
from queries.user import get_user_by_id
from schemas.graphql.product import (
    CreateProductResponse,
    DeleteProductResponse,
    GetProductResponse,
    UpdateProductResponse,
)
from schemas.pydantic.product import ProductChange, ProductSchema
from services.email import send_plain_email
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from utils.email import generate_html_change_product
from utils.extras import clean_dict, diff_dict


def _send_email_for_change_product(product_change: ProductChange):
    body = generate_html_change_product(product_change)
    print(body)
    send_plain_email(
        product_change.email,
        f"Change in Product with sku {product_change.sku}",
        body,
    )


def get_product(db: Session, sku: str, user_id: int) -> GetProductResponse:
    try:
        product_data = get_product_by_sku(db, sku)
    except NoResultFound:
        raise ProductNotFound(sku)

    user_data = get_user_by_id(db, user_id)

    create_product_tacking(
        db, ProductTracking(user_id=user_data.id, product_id=product_data.id)
    )

    return GetProductResponse(**product_data.normalize())


def add_product(db: Session, product: ProductSchema) -> CreateProductResponse:
    try:
        if get_product_by_sku(db, product.sku):
            raise ProductDuplicated(product.sku)
    except NoResultFound:
        pass

    product_data = create_product(db, Product(**product.__dict__))

    return CreateProductResponse(**product_data.normalize())


def updated_product(
    db: Session, product: ProductSchema, email: str, user_id: int
) -> UpdateProductResponse:
    try:
        product_data = get_product_by_sku(db, product.sku)
    except NoResultFound:
        raise ProductNotFound(product.sku)

    update_data = clean_dict(product.__dict__)
    diff_data = diff_dict(product_data.normalize(), update_data)

    if diff_data:
        _send_email_for_change_product(
            ProductChange(
                email=email,
                user_id=user_id,
                sku=product_data.sku,
                product_id=product_data.id,
                product_change=diff_data,
            )
        )

    update_product(db, product_data.id, Product(**update_data))
    return UpdateProductResponse(**product_data.normalize())


def deleted_product(db: Session, sku: str) -> DeleteProductResponse:
    try:
        product_data = get_product_by_sku(db, sku)
    except NoResultFound:
        raise ProductNotFound(sku)

    delete_product(db, product_data.id)
    return DeleteProductResponse(
        **product_data.normalize(), message="Product deleted successfully"
    )
