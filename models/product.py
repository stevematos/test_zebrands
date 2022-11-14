from models.base_model import TimestampedBase, EntityBase
# from models.base_model import EntityBase

from sqlalchemy import Column, ForeignKey, func
from sqlalchemy import Integer, String, Float, DateTime


class Product(TimestampedBase):
    __tablename__ = "product"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(255), nullable=False)
    sku = Column(String(255), nullable=False, unique=True)
    price = Column(Float(8, 2), nullable=False)
    brand = Column(String(255))


class ProductTracking(EntityBase):
    __tablename__ = "product_tracking"

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    product_id = Column(Integer, ForeignKey("product.id"))
    created_at = Column(
        DateTime, nullable=False, default=func.now(), server_default=func.now()
    )

