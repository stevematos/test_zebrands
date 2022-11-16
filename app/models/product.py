from models.base_model import EntityBase, TimestampedBase
from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    func,
)


class Product(TimestampedBase):
    __tablename__ = "product"

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(255), nullable=False)
    sku = Column(String(255), nullable=False, unique=True)
    price = Column(Float(8, 2), nullable=False)
    brand = Column(String(255))

    def normalize(self):
        return {
            "name": self.name.__str__(),
            "sku": self.sku.__str__(),
            "price": self.price,
            "brand": self.brand.__str__(),
        }


class ProductTracking(EntityBase):
    __tablename__ = "product_tracking"

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    product_id = Column(Integer, ForeignKey("product.id"))
    created_at = Column(
        DateTime,
        nullable=False,
        default=func.now(),
        server_default=func.now(),
    )
