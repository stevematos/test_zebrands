from typing import Optional
from pydantic import BaseModel


class ProductSchema(BaseModel):
    sku: str
    name:  Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None


class ProductChange(BaseModel):
    email: str
    sku: str
    user_id: int
    product_id: int
    product_change: dict
