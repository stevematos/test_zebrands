from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from models import Product, ProductTracking
from queries.product import get_product_by_sku, create_product, update_product, delete_product, create_product_tacking
from queries.user import get_user_by_email
from schemas.graphql.product import CreateProductResponse, UpdateProductResponse, DeleteProductResponse, \
    GetProductResponse
from schemas.pydantic.product import ProductSchema
from config.exceptions import ProductDuplicated, ProductNotFound
from utils.extras import clean_dict


def get_product(db: Session, sku: str, email: str) -> GetProductResponse:
    try:
        product_data = get_product_by_sku(db, sku)
    except NoResultFound:
        raise ProductNotFound(sku)

    user_data = get_user_by_email(db, email)

    create_product_tacking(
        db,
        ProductTracking(
            user_id=user_data.id,
            product_id=product_data.id
        )
    )

    return GetProductResponse(
        sku=product_data.sku,
        name=product_data.name,
        price=product_data.price,
        brand=product_data.brand
    )


def add_product(db: Session, product: ProductSchema) -> CreateProductResponse:
    try:
        if get_product_by_sku(db, product.sku):
            raise ProductDuplicated(product.sku)
    except NoResultFound:
        pass

    db_user = create_product(db, Product(**product.__dict__))

    return CreateProductResponse(
        sku=db_user.sku,
        name=db_user.name,
        price=db_user.price,
        brand=db_user.brand
    )


def updated_product(db: Session, product: ProductSchema) -> UpdateProductResponse:
    try:
        product_data = get_product_by_sku(db, product.sku)
    except NoResultFound:
        raise ProductNotFound(product.sku)

    update_data = clean_dict(product.__dict__)

    update_product(db, product_data.id, Product(**update_data))
    return UpdateProductResponse(
        name=product_data.name,
        price=product_data.price,
        brand=product_data.brand
    )


def deleted_product(db: Session, sku: str) -> DeleteProductResponse:
    try:
        product_data = get_product_by_sku(db, sku)
    except NoResultFound:
        raise ProductNotFound(sku)

    delete_product(db, product_data.id)
    return DeleteProductResponse(
        sku=product_data.sku,
        name=product_data.name,
        price=product_data.price,
        brand=product_data.brand,
        message="Product deleted successfully"
    )
