from sqlalchemy.orm import Session

from models.product import Product, ProductTracking


def get_product_by_sku(db: Session, sku: str) -> Product:
    return db.query(Product).filter(Product.sku == sku).one()


def create_product(db: Session, product: Product) -> Product:
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def update_product(db: Session, _id: int, product: Product):
    product.id = _id
    db.merge(product)
    db.commit()


def delete_product(db: Session, _id: int):
    db.query(Product).filter(Product.id == _id).delete()
    db.commit()
    db.flush()


def create_product_tacking(
    db: Session, product_tracking: ProductTracking
) -> ProductTracking:
    db.add(product_tracking)
    db.commit()
    db.refresh(product_tracking)
    return product_tracking
